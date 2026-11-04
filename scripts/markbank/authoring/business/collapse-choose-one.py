"""Choice is not a route, refined: the six choose-one Business pools become ONE card each.

Refinement (AGENT-BRIEF, 2026-10-12): a choose-one pool keeps one card per
option only when the scheme marks the options differently or they file under
different syllabus topics. All six share one grid and one topic, so each is
one card. The rest of this note describes the N >= 2 pass this script reuses.

Choice is not a route: collapse every choose-N (N >= 2) Business pool to ONE card.

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


WORDS = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five'}
ORD = ['First', 'Second', 'Third', 'Fourth']

# pool id -> (noun, plural, directive mode, requirement, kept guidance, [(item, scheme page, quote)])
#   mode 'sw'       question text is the printed directive, which names the items itself
#   mode 'ctx+sw'   context lines, then the printed directive (items named in it or above)
#   mode 'ctx+sw+L' context lines, the printed directive, then every printed item
SPEC = {
    'bus-2015-hl-s3-q4a-i': ('chart', 'charts', 'text2015',
        'Choose a bar chart or a line graph and draw it: 1 mark for each of the six bars or points, 2 for the title and 2 for each axis.',
        ['The graph earns 12 marks. The remaining 13 marks in Part (A) are for the separate communication-principles task.'],
        [('Bar chart', 34, 'Projected Sales of Water Conservation product Revenue July - December 2015'),
         ('Line graph', 34, 'Projected Sales of Water Conservation product Revenue July - December 2015')]),
    'bus-2024-hl-s3-q3cii': ('policy', 'policies', 'bullets2024',
        'Choose one of the three printed policies and explain two points of its importance for Ireland at 5 marks each (2 + 3).', [],
        [('Common Agricultural Policy', 41, 'The Common Agricultural Policy gives grants farmers under the single payment scheme.'),
         ('EU Social Policy', 42, 'Workers have the right to migrate freely which benefits employers in terms of recruitment and selection.'),
         ('EU Competition Policy', 42, 'It restricts Irish businesses from forming anti-competitive cartels or keeping prices artificially high or preventing newcomers from entering the market.')]),
    'bus-2022-hl-s3-q2a': ('company type', 'company types', 'or2022',
        'Choose one of the two printed company types and evaluate it: three features at 6 marks each (3 + 3) and 2 marks for evaluation.', [],
        [('A Private Company Limited by shares (LTD company)', 31, 'The following apply to both types of limited companies; Limited Liability: The shareholders of a private limited company have limited liability.'),
         ('A Designated Activity Company (DAC)', 31, 'The following apply to both types of limited companies; Limited Liability: The shareholders of a private limited company have limited liability.')]),
    'bus-2026-ol-s2-q3a': ('chart', 'charts', 'ctx+sw',
        'Choose a bar chart or a line graph: title 1, labelled axes 2 + 2, and each of the five values at 2 marks (1 each if not to scale).',
        ['Scheme: “(1m each if not to scale)” for each bar or point. The figures are read from the printed table.'],
        [('Bar Chart', 19, '5 Bars @ 2m each (1m each if not to scale)'),
         ('Line Graph', 19, '5 Pts @ 2m each (1m each if not to scale)')]),
    'bus-2025-ol-s2-q3e': ('institution', 'institutions', 'ctx+sw+L',
        'Choose one of the three printed institutions and explain its role: 10 + 5.',
        ['The scheme allocates the explanation 10 + 5 without fixing either amount to a particular role point.'],
        [('European Parliament', 23, 'Legislates, debates and votes on all new laws and policies proposed by the Commission before they may become law.'),
         ('European Commission', 23, 'Responsible for the day-to-day management of the EU. It is the executive body of the EU.'),
         ('Council of the European Union', 23, 'Sets goals and plans for the EU.')]),
    'bus-2023-ol-s2-q6e': ('role', 'roles', 'tail2023',
        'Choose one of the two printed roles and explain it: 10 marks (5 + 5).', [],
        [('Assessors', 27, 'an assessor calculates the compensation for a claim made.'),
         ('Actuaries', 27, 'an actuary is responsible for calculating the insurance premium.')]),
}

pools_path = Path('components/MarkBank/cards/business/route-pools.json')
rp = json.loads(pools_path.read_text())
routes = json.loads(subprocess.check_output(['node', 'scripts/markbank/authoring/business_routes.mjs'], text=True))
route_ids = {}
for r in routes:
    route_ids.setdefault(r['routePoolId'], []).append(r['id'])

collapse = [p for p in rp['pools'] if p['id'] in SPEC]
assert len(collapse) == 6 and all(p['choose'] == 1 for p in collapse)
for p in collapse:
    assert len({o['topicId'] for o in p['options']}) == 1, p['id']
assert [p['id'] for p in rp['pools'] if p['id'] not in SPEC] == ['bus-2013-hl-s3-q1b']

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
    elif mode == 'text2015':
        paul = 'Paul O’Brien is the Sales Manager with Water Solutions Ltd, a business which has recently developed a new water conservation product. Paul is due to make a presentation to the board of directors on the potential of this product. He will present the following projected sales data for the product for the next six months.'
        table = ['Month: July August September October November December', 'Sales in €: 50,000 60,000 40,000 30,000 20,000 10,000']
        for piece in [paul] + table + ['(i) ' + sw]:
            assert piece in paper_text, piece
        text = paul + '\n' + '\n'.join(table) + '\n\n(i) ' + sw
    elif mode == 'bullets2024':
        text = sw + '\n' + '\n'.join('• ' + o['label'] for o in p['options'])
        assert norm(sw + ' ' + ' '.join('• ' + o['label'] for o in p['options'])) in paper_text
    elif mode == 'or2022':
        text = prefix + sw + '\n' + '\nor\n'.join(o['label'] for o in p['options'])
        assert norm(sw + ' ' + ' or '.join(o['label'] for o in p['options'])) in paper_text
    elif mode == 'tail2023':
        last = lines[-1]
        lead = last[:last.index('Explain the role of the following')].rstrip()
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
    guidance = [f'You choose one of the {WORDS[m]} printed {plural} to answer. The scheme marks every choice alike and files them under one topic, so this is one card whichever {noun} you choose.'] + kept
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
    responses = [dict(id=f'response-{i}', label=f'The {noun} you chose',
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
        card['correction'] = dict(legacy['correction'], reason=head + f': question text lifted from the printed paper, with all {WORDS[m]} printed {plural}; the printed choice of one is ONE card (the scheme marks every option alike under one topic), with criteria for the chosen {noun} and the scheme’s wording for every {noun}. Retain the existing card ID and total marks for saved progress.')
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
    # The N >= 2 pass left one "Still routed ..." sentence naming these pools.
    keep = [s for s in re.split(r'(?<=\.)\s+', text) if not s.startswith('Still routed')]
    add = 'Choose-one printed choices marked alike under one topic are one card each: ' + '; '.join(sorted(by_section[key])) + '.'
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
        r['reason'] = f"{info['desc']}: the candidate chooses one; the scheme marks every option alike and they share one topic, so one card carries every printed option."
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
        kept = [s for s in re.split(r'(?<=\.)\s+', note) if not s.startswith('Still routed')]
        if kept:
            notes.append(' '.join(kept))
    notes.insert(min(2, len(notes)), 'Choose-one choice marked alike under one topic: ' + '; '.join(sorted(info['desc'] for info in hit))
                 + (' are ONE card each' if len(hit) > 1 else ' is ONE card') + ', printing every option, with the scheme’s wording for every option.')
    review['reviewNotes'] = notes
pr_path.write_text(json.dumps(prs, ensure_ascii=False, indent=2) + '\n')

print(f'collapsed {len(cards)} choose-one pools into one card each, removing {sum(len(i["routes"]) for i in card_of.values())} route cards; '
      f'{moved} selection reviews now name their card; {len(rp["pools"])} pools remain')
