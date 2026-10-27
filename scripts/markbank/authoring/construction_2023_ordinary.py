"""Source-pinned validator for the 2023 Ordinary Level Construction Studies theory paper (Q1-Q9).

Checks the reviewed authoring file against the original SEC paper and marking scheme
(byte-identical paper-trail-corpus copies, pinned by SHA-256): page text, lifted question
wording (narrowing only deletes printed words), scheme-traceable rows, the published tariffs
and mark steps, the Q8 choice as ONE any-five card over all nine printed terms (choice is not a
route: no per-term or per-combination cards), pixel-exact figure crops (the Q8 terms as one
composite of the three scheme pages), the selection ledger and exact topic/Atlas bindings.
Of the 27 pre-audit 2023 Ordinary cards, 19 keep their IDs and concept IDs and are corrected in
place (hash-linked to the card each replaced); the other eight per-term Q8 cards are withdrawn into
the surviving Q8 card through recorded progress aliases. Every other prior card stays byte-identical.
"""
import copy
import hashlib
import json
import re
from pathlib import Path

import fitz

import construction_corrections
import construction_figures

R = Path(__file__).resolve().parents[3]
REVIEW = R / 'scripts/markbank/authored/construction-studies-2023-ordinary-reviewed.json'
DRAFTS = R / 'docs/markbank-audit/2026-09-28/drafts/construction-2023-ordinary'
FIGURE_DIR = R / 'public/exam-figures/construction-studies/markbank'
P = 'paper-trail-corpus/exampapers/2023/LC029GLP000EV.pdf'
S = 'paper-trail-corpus/markingschemes/2023/LC029GLP000EV.pdf'
HASHES = {P: 'e0a846a2ce2454b807ef95754ed579c79a7a6cb468a158e68ad50991441e8db9',
          S: '1018b8c0eada563d4713dab8ec9b219d47a1cec60e2b84b56e536f9222195025'}
PREFIX = 'cons-2023-ol-'
FP = 'construction-studies-2023-OL-'
CROSS = 'construction-studies-ordinary-'
BAND8 = [0, 4, 6, 8]
BAND6 = [0, 2, 4, 6]
Q8 = 'q8-None-concrete-mixer'
TERM_ITEMS = ['concrete mixer', 'smart radiator valve', 'ridge tile', 'triple glazing', 'balusters', 'cedar cladding',
              'bridle joint', 'wood pellet stove', 'floor screed']
TERM_HEADINGS = ['Concrete mixer', 'Smart radiator valve', 'Ridge tile', 'Triple glazing', 'Balusters', 'Cedar cladding',
                 'Bridle joint', 'Wood pellet stove', 'Floor screed']
PRIOR_COUNT = 759
LEGACY = {'q1-a', 'q1-b', 'q2-a', 'q2-c', 'q3-a', 'q3-b', 'q4-a', 'q4-b', 'q5-a', 'q5-b', 'q6-a', 'q6-b', 'q6-c', 'q7-a', 'q7-b',
          'q9-a', 'q9-b', 'q9-c', Q8}
CONSOLIDATED = {f'q8-None-{t}': Q8 for t in ['smart-radiator-valve', 'ridge-tile', 'triple-glazing', 'balusters', 'cedar-cladding',
                                            'bridle-joint', 'wood-pellet-stove', 'floor-screed']}


def r(n):
    return list(range(n + 1))


CHOICES = {}
CHOICES.update({'q1-a': ('details', 7, 5, ["Concrete block outer leaf with internal plaster", "Full fill cavity with wall tie", "Concrete block inner leaf with render", "Joist hanger", "Ceiling joist", "Airtight tape", "Plasterboard", "Plywood decking", "Tongue & groove flooring", "Skirting board"]), 'q3-a': ('details', 8, 5, ["Solar collector", "Cold feed to collector", "Hot return to cylinder", "Cylinder", "Circulation pump", "Solar expansion vessel", "Storage tank", "Cold feed to cylinder", "Expansion pipe", "Hot water to shower and shower unit", "Valves"]), 'q5-a': ('details', 8, 5, ["Concrete block outer leaf with external render", "Full fill insulated cavity with wall tie", "Concrete block inner leaf with internal plaster", "Wall plate with cavity closer", "Waterproof membrane", "Insulation", "Plywood decking with breather membrane", "Firring piece", "Insulated ceiling joist", "Insulated plasterboard ceiling with airtight membrane", "Fascia and soffit", "Gutter"])})  # drawing details as option groups (construction_choices.py)
LEAF = {
    'q1-a': [('details', 35, None), ('dimensions', 4, r(4)), ('presentation', 8, BAND8)],
    'q1-b': [('wall-tie', 3, [0, 3])],
    'q2-a': [('reason-1', 6, r(6)), ('reason-2', 6, r(6))],
    'q2-b': [('method', 16, r(16)), ('type', 4, r(4)), ('thickness', 4, r(4))],
    'q2-c': [('upgrade', 14, r(14))],
    'q3-a': [('details', 40, None)],
    'q3-b': [('consideration-1', 5, r(5)), ('consideration-2', 5, r(5))],
    'q4-a': [('advantage-1', 4, r(4)), ('advantage-2', 4, r(4))],
    'q4-b': [(k, 6, r(6)) for k in ['wall', 'wallplate', 'rafter', 'nail-plate', 'truss-clip']],
    'q4-c': [('material', 4, r(4)), ('reason-1', 4, r(4)), ('reason-2', 4, r(4))],
    'q5-a': [('details', 40, None), ('presentation', 6, BAND6)],
    'q5-b': [('closer', 4, [0, 4])],
    'q6-a': [(k, 4, r(4)) for k in ['jigsaw-1', 'jigsaw-2', 'epoxy-1', 'epoxy-2']],
    'q6-b': [(f'precaution-{i}', 8, r(8)) for i in (1, 2, 3)],
    'q6-c': [('reason-1', 5, r(5)), ('reason-2', 5, r(5))],
    'q7-a': [('advantage-1', 5, r(5)), ('advantage-2', 5, r(5))],
    'q7-b': [('sketch', 8, r(8))] + [(k, 5, r(5)) for k in ['sink', 'washing-machine', 'storage', 'seating']],
    'q7-c': [('covering', 4, r(4)), ('reason-1', 4, r(4)), ('reason-2', 4, r(4))],
    Q8: [('terms', 50, None)],
    'q9-a': [('material', 4, r(4)), ('reason-1', 4, r(4)), ('reason-2', 4, r(4))],
    'q9-b': [('modification-1', 13, r(13)), ('modification-2', 13, r(13))],
    'q9-c': [('reason-1', 6, r(6)), ('reason-2', 6, r(6))],
}
COMPOSITE = {
    'q1-complete': ['q1-a', 'q1-b'], 'q2-complete': ['q2-a', 'q2-b', 'q2-c'], 'q3-complete': ['q3-a', 'q3-b'],
    'q4-complete': ['q4-a', 'q4-b', 'q4-c'], 'q5-complete': ['q5-a', 'q5-b'], 'q6-complete': ['q6-a', 'q6-b', 'q6-c'],
    'q7-complete': ['q7-a', 'q7-b', 'q7-c'], 'q9-complete': ['q9-a', 'q9-b', 'q9-c'],
}
TOTALS = {'q1-a': 47, 'q1-b': 3, 'q2-a': 12, 'q2-b': 24, 'q2-c': 14, 'q3-a': 40, 'q3-b': 10, 'q4-a': 8, 'q4-b': 30, 'q4-c': 12,
          'q5-a': 46, 'q5-b': 4, 'q6-a': 16, 'q6-b': 24, 'q6-c': 10, 'q7-a': 10, 'q7-b': 28, 'q7-c': 12, Q8: 50,
          'q9-a': 12, 'q9-b': 26, 'q9-c': 12, **{k: 50 for k in COMPOSITE}}
SCHEME_PAGES = {'1': [4, 16], '2': [5, 17], '3': [6, 18], '4': [7, 19], '5': [8, 20], '6': [9, 21],
                '7': [10, 11, 22], '8': [12, 13, 14, 23], '9': [15, 24]}
PAPER_PAGE = {'1': 2, '2': 2, '3': 2, '4': 3, '5': 3, '6': 3, '7': 4, '8': 4, '9': 4}


def composite(*panels):
    return construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [45, 39, 580, 288], False), 'q2-original': (P, 2, [45, 288, 580, 530], False),
    'q3-original': (P, 2, [45, 530, 580, 767], False), 'q4-original': (P, 3, [45, 39, 580, 312], False),
    'q5-original': (P, 3, [45, 312, 580, 585], False), 'q6-original': (P, 3, [45, 585, 580, 767], False),
    'q7-original': (P, 4, [45, 39, 580, 386], False), 'q8-original': (P, 4, [45, 386, 580, 480], False),
    'q9-original': (P, 4, [45, 527, 580, 767], False),
    'q1-scheme': (S, 4, [51, 58, 545, 722], True),
    'q2-reasons': (S, 5, [51, 58, 540, 188], True), 'q2-method': (S, 5, [51, 188, 540, 566], True),
    'q2-upgrade': (S, 5, [51, 566, 540, 770], True),
    'q3-system': (S, 6, [51, 58, 545, 560], True), 'q3-locations': (S, 6, [51, 588, 545, 768], True),
    'q4-advantages': (S, 7, [51, 58, 545, 198], True), 'q4-fixing': (S, 7, [51, 198, 545, 472], True),
    'q4-finishes': (S, 7, [51, 474, 552, 782], True),
    'q5-section': (S, 8, [51, 58, 545, 615], True), 'q5-closer': (S, 8, [51, 615, 545, 792], True),
    'q6-classroom': (S, 9, [51, 58, 545, 334], True), 'q6-lathe': (S, 9, [51, 334, 545, 610], True),
    'q6-tidy': (S, 9, [51, 610, 545, 780], True),
    'q7-advantages': (S, 10, [51, 58, 545, 210], True),
    'q7-layout': composite((10, [51, 212, 545, 712]), (11, [51, 50, 545, 392])),
    'q7-covering': (S, 11, [51, 394, 545, 740], True),
    'q8-terms': composite((12, [51, 58, 545, 797]), (13, [51, 50, 545, 722]), (14, [51, 50, 545, 764])),
    'q9-materials': (S, 15, [51, 58, 545, 340], True), 'q9-modifications': (S, 15, [51, 340, 545, 566], True),
    'q9-reasons': (S, 15, [51, 566, 545, 776], True),
}
SOLUTION = {'q1-a': 'q1-scheme', 'q1-b': 'q1-scheme', 'q1-complete': 'q1-scheme', 'q2-a': 'q2-reasons', 'q2-b': 'q2-method',
            'q2-c': 'q2-upgrade', 'q2-complete': 'q2-method', 'q3-a': 'q3-system', 'q3-b': 'q3-locations', 'q3-complete': 'q3-system',
            'q4-a': 'q4-advantages', 'q4-b': 'q4-fixing', 'q4-c': 'q4-finishes', 'q4-complete': 'q4-fixing',
            'q5-a': 'q5-section', 'q5-b': 'q5-closer', 'q5-complete': 'q5-section',
            'q6-a': 'q6-classroom', 'q6-b': 'q6-lathe', 'q6-c': 'q6-tidy', 'q6-complete': 'q6-lathe',
            'q7-a': 'q7-advantages', 'q7-b': 'q7-layout', 'q7-c': 'q7-covering', 'q7-complete': 'q7-layout', Q8: 'q8-terms',
            'q9-a': 'q9-materials', 'q9-b': 'q9-modifications', 'q9-c': 'q9-reasons', 'q9-complete': 'q9-modifications'}
SAFETY = (['cons-9-4'], ['site-safety'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-3-3', 'cons-4-3'], ['question-one-drawing-questions', 'foundations-floors-walls']),
    'q1-b': (['cons-3-3'], ['foundations-floors-walls']),
    'q2-a': (['cons-6-3', 'cons-1-2'], ['heat-loss-insulation', 'planning-sustainability-environment']),
    'q2-b': (['cons-6-2', 'cons-3-3'], ['heat-loss-insulation', 'foundations-floors-walls']),
    'q2-c': (['cons-6-2', 'cons-5-3'], ['heat-loss-insulation', 'hot-water-space-heating']),
    'q3-a': (['cons-5-2', 'cons-6-4'], ['hot-water-space-heating', 'planning-sustainability-environment']),
    'q3-b': (['cons-6-4', 'cons-3-9'], ['planning-sustainability-environment', 'roofs']),
    'q4-a': (['cons-3-8'], ['roofs']),
    'q4-b': (['cons-3-8', 'cons-3-10', 'cons-3-3'], ['roofs', 'foundations-floors-walls']),
    'q4-c': (['cons-3-9'], ['roofs']),
    'q5-a': (['cons-1-5', 'cons-3-10', 'cons-3-3', 'cons-6-2'], ['question-one-drawing-questions', 'roofs', 'foundations-floors-walls', 'heat-loss-insulation']),
    'q5-b': (['cons-3-3', 'cons-6-2'], ['foundations-floors-walls', 'heat-loss-insulation']),
    'q6-a': SAFETY, 'q6-b': SAFETY, 'q6-c': SAFETY,
    'q7-a': (['cons-1-2'], ['planning-sustainability-environment']),
    'q7-b': (['cons-1-2'], ['planning-sustainability-environment']),
    'q7-c': (['cons-4-2', 'cons-1-2'], ['foundations-floors-walls', 'planning-sustainability-environment']),
    Q8: (['cons-2-7', 'cons-5-3', 'cons-3-9', 'cons-3-6', 'cons-6-2', 'cons-4-4', 'cons-3-2', 'cons-10-1', 'cons-10-4', 'cons-1-2', 'cons-4-2'],
         ['concrete', 'hot-water-space-heating', 'services-water-gas-electrical', 'roofs', 'windows-doors', 'heat-loss-insulation',
          'foundations-floors-walls', 'wood-rot-ventilation', 'planning-sustainability-environment']),
    'q9-a': (['cons-3-7'], ['windows-doors']),
    'q9-b': (['cons-1-2', 'cons-3-7'], ['planning-sustainability-environment', 'windows-doors']),
    'q9-c': (['cons-1-2'], ['planning-sustainability-environment']),
}
GAPS = {Q8: {'cons-4-4', 'cons-10-1', 'cons-10-4'}}


def tokens(text):
    return re.findall(r'[a-z0-9]+', text.replace('²', '2').lower())


def is_subsequence(needle, haystack):
    it = iter(haystack)
    return all(word in it for word in needle)


def normalise(text):
    return re.sub(r'[^a-z0-9Ā-ſ]+', '', text.lower())


def page_text(f, page):
    with fitz.open(R / f) as pdf:
        return ' '.join(pdf[page - 1].get_text().split())


def region(q):
    text = page_text(P, PAPER_PAGE[q])
    start = text.index(f' {q}. ')
    later = [text.index(f' {n}. ') for n in '123456789' if int(n) > int(q) and f' {n}. ' in text]
    body = text[start:min(later) if later else len(text)]
    if q == '8':  # the text layer places Q8's three-column term list after Q9
        body += text[text.index('accessible for all.') + len('accessible for all.'):]
    return body


def validate(d, images=True, figure_dir=FIGURE_DIR, integrated=True):
    assert d['sourceHashes'] == HASHES
    for f, h in HASHES.items():
        assert hashlib.sha256((R / f).read_bytes()).hexdigest() == h, f
    assert (d['subjectId'], d['year'], d['level'], d['lang'], d['sitting'], d['paperKey'], d['fileid']) == (
        'construction-studies', 2023, 'ordinary', 'ev', 'main', 'single', 'LC029GLP000EV.pdf')
    cards = {t['card']['id'].removeprefix(PREFIX): t['card'] for t in d['tasks']}
    tasks = {t['card']['id'].removeprefix(PREFIX): t for t in d['tasks']}
    expected = set(LEAF) | set(COMPOSITE)
    assert set(cards) == expected and len(d['tasks']) == len(expected) == 30
    assert d['addedIds'] == [t['card']['id'] for t in d['tasks'] if t['card']['id'].removeprefix(PREFIX) not in LEGACY]
    assert len(d['addedIds']) == 11 and all(t['correction'] == (k in LEGACY) for k, t in tasks.items())
    assert len({c['questionRef'] for c in cards.values()}) == 30
    bindings = {b['cardId'].removeprefix(PREFIX): b for b in d['bindings']}
    assert set(bindings) == expected and len(d['bindings']) == 30
    scheme = normalise(' '.join(page_text(S, p) for p in range(1, 25)))
    crosswalk = json.loads((R / 'data/examTopics/construction-studies-curriculum-crosswalk.json').read_text())
    registry = set(re.findall(r"id: '(cons-\d+-\d+)'", (R / 'curriculumRegistry.ts').read_text()))
    library_nodes = {n for nodes in crosswalk.values() for n in nodes}
    figures = {f['key'].removeprefix(FP): f for f in d['questionFigures']}
    assert set(figures) == set(FIGURES) and len(d['questionFigures']) == 30

    for key, c in cards.items():
        q = key[1]
        t, b = tasks[key], bindings[key]
        assert t['questionNumber'] == b['questionNumber'] == q
        assert (c['subjectId'], c['year'], c['level'], c['section']) == ('construction-studies', 2023, 'ordinary', 'B')
        assert c['tariffModel'] == {'kind': 'fixed'} and c['questionRef'].startswith(f'2023 OL Q{q}')
        assert c['questionFigureKey'] == f'{FP}q{q}-original' and c['questionFigureIncludesPrompt'] is True
        assert c['sourceMaterial']['pages'] == [1, PAPER_PAGE[q]] and t['requiredQuestionFigures'] == [c['questionFigureKey']]
        assert c.get('figureKey') == (FP + SOLUTION[key] if key in SOLUTION else None), key
        assert t['requiredSolutionFigures'] == ([FP + SOLUTION[key]] if key in SOLUTION else [])
        assert figures[f'q{q}-original']['solution'] is False and (key not in SOLUTION or figures[SOLUTION[key]]['solution'] is True)
        words = tokens(region(q))
        assert is_subsequence(tokens(c['questionText']), words), (key, 'questionText not lifted')
        assert is_subsequence(tokens(c['stem']), words), (key, 'stem not lifted')
        for row in c['rows']:
            assert row['contextNote'].strip()
            if row['kind'] == 'anyN':  # a closed choice: every printed option, in the scheme's own headings
                assert 'permittedMarks' not in row and row['marks'] == row['group']['claimMax'] * row['group']['perOption'], (key, row['id'])
                assert normalise(row['verbatim']) in scheme and all(normalise(o) in scheme for o in row['group']['options']), key
                continue
            assert row['kind'] == 'criterion'
            assert normalise(row['verbatim']) in scheme, (key, row['verbatim'])
            steps = row['permittedMarks']
            assert steps[0] == 0 and steps[-1] == row['marks'] and steps == sorted(set(steps)), (key, row['id'])
        assert 'questionBonus' not in c and c['totalMarks'] == sum(row['marks'] for row in c['rows']) == TOTALS[key], key
        if key in LEAF:
            assert [(row['id'], row['marks'], row.get('permittedMarks')) for row in c['rows']] == LEAF[key], key
            assert 'taskGroups' not in c
            nodes, topics = TOPICS[key]
            assert b['canonicalTopicIds'] == nodes and b['atlasTopicIds'] == [CROSS + x for x in topics], key
            covered = {n for x in b['atlasTopicIds'] for n in crosswalk[x]}
            assert set(nodes) - covered == GAPS.get(key, set()), (key, 'canonical topics outside Atlas crosswalk')
        else:
            kids = COMPOSITE[key]
            assert [g['sourceCardId'] for g in c['taskGroups']] == [PREFIX + k for k in kids] and len(kids) >= 2
            rows = []
            for kid, g in zip(kids, c['taskGroups']):
                rs = copy.deepcopy(cards[kid]['rows'])
                for row in rs:
                    row['id'] = kid.removeprefix(f'q{q}-') + '-' + row['id']
                assert g['rowIds'] == [row['id'] for row in rs] and g['marks'] == cards[kid]['totalMarks'] and len(rs) <= 5 and g['label'].strip()
                rows += rs
            assert c['rows'] == rows, key
            assert b['canonicalTopicIds'] == list(dict.fromkeys(n for k in kids for n in bindings[k]['canonicalTopicIds']))
            assert b['atlasTopicIds'] == list(dict.fromkeys(x for k in kids for x in bindings[k]['atlasTopicIds']))
        assert b['markBankTopicId'] == c['topicId'] == b['canonicalTopicIds'][0]
        assert set(b['canonicalTopicIds']) <= registry & library_nodes and len(set(b['canonicalTopicIds'])) == len(b['canonicalTopicIds'])
        assert all(x.startswith(CROSS) and x in crosswalk for x in b['atlasTopicIds']) and b['atlasTopicIds']
        assert len(b['canonicalTopicIds']) == 1 or b['canonicalTopicReview'].strip()
        assert [(x['file'], x['page']) for x in t['sourceChecks']] == [(P, 1), (P, PAPER_PAGE[q])] + [(S, p) for p in [2, 3, *SCHEME_PAGES[q]]], key
        for x in t['sourceChecks']:
            assert hashlib.sha256(page_text(x['file'], x['page']).encode()).hexdigest() == x['textSha256'], (key, x)

    # Choice is not a route: Q8 is ONE card printing all nine terms, with one any-five group over them.
    q8 = cards[Q8]
    assert [k for k in cards if k.startswith('q8')] == [Q8] and 'taskGroups' not in q8
    assert q8['questionText'].endswith('any five of the following: ' + '; '.join(TERM_ITEMS) + '.')
    assert q8['rows'][0]['kind'] == 'anyN' and q8['rows'][0]['group'] == dict(claimMax=5, perOption=10, options=TERM_HEADINGS)
    sel = d['selectionLedger']
    assert sel['finiteQuestionChoices']['8']['cardId'] == PREFIX + Q8 and 'routes' not in sel['finiteQuestionChoices']['8']
    assert sel['unclassified'] == 0 and all(x['classification'] for x in sel['rows'])
    observed = []
    with fitz.open(R / P) as pdf:
        for i, p in enumerate(pdf):
            observed.extend((i + 1, m.start(), m.group()) for m in re.finditer(sel['pattern'], ' '.join(p.get_text().split()), re.I))
    assert observed == [(x['page'], x['start'], x['match']) for x in sel['rows']] and len(observed) == 2
    for q in '123456789':
        whole = [Q8] if q == '8' else [k for k in cards if k.startswith(f'q{q}-complete')]
        assert whole and {w['id'] for w in d['questionRouteLedgers'][q]['wholeRoutes']} == {PREFIX + k for k in whole}

    for key, f in figures.items():  # pixel-exact: a single crop, or a composite of the scheme pages carrying every term
        construction_figures.check(f, FIGURES[key], figure_dir, images)
    assert len({f['sha256'] for f in d['questionFigures']}) == 30

    # In-place corrections: same ID and concept ID, hash-linked to the pre-audit card they replace.
    legacy = {c['id']: c for c in json.loads((DRAFTS / 'prior-2023-ordinary-cards.json').read_text())}
    assert set(legacy) == {PREFIX + k for k in LEGACY | set(CONSOLIDATED)}
    fixes = {x['cardId']: x for x in d['corrections']}
    assert set(fixes) == {PREFIX + k for k in LEGACY} and len(d['corrections']) == 19
    merged = {x['cardId']: x for x in d['consolidatedLegacy']}
    assert merged == {PREFIX + k: dict(cardId=PREFIX + k, aliasOf=PREFIX + v, preCorrectionSha256=construction_corrections.card_hash(legacy[PREFIX + k]))
                      for k, v in CONSOLIDATED.items()}
    for cid, old in legacy.items():
        if cid in merged:
            continue
        new = cards[cid.removeprefix(PREFIX)]
        fix = fixes[cid]
        assert fix['priorSha256'] == construction_corrections.card_hash(old) and fix['correctedSha256'] == construction_corrections.card_hash(new), cid
        assert new['conceptId'] == old['conceptId'] and fix['reason'].strip(), cid
        assert (fix['priorTotalMarks'], fix['correctedTotalMarks'], fix['priorTopicId'], fix['correctedTopicId']) == (
            old['totalMarks'], new['totalMarks'], old['topicId'], new['topicId']), cid

    authored = json.loads((R / 'scripts/markbank/authored/construction-studies.json').read_text())
    by_id = {c['id']: c for c in authored}
    assert len(by_id) == len(authored)
    if integrated:
        prior = json.loads((DRAFTS / 'prior-authored-card-hashes.json').read_text())
        assert prior['count'] == len(prior['cards']) == PRIOR_COUNT
        for cid in fixes:
            assert prior['cards'][cid] == fixes[cid]['priorSha256'], cid
        construction_corrections.assert_prior_cards_preserved(prior['cards'], by_id)
        assert all(by_id[t['card']['id']] == t['card'] for t in d['tasks'])
        assert sorted(c for c in by_id if c.startswith(PREFIX)) == sorted(t['card']['id'] for t in d['tasks'])
        # The eight per-term cards are withdrawn through a recorded progress alias to the surviving Q8 card.
        gone = {w['cardId']: w for w in d.get('withdrawn', [])}
        aliases = construction_corrections.card_aliases()
        assert set(gone) == set(merged)
        for cid, m in merged.items():
            assert cid not in by_id and gone[cid]['aliasOf'] == m['aliasOf'] == aliases[cid], cid
            assert gone[cid]['priorSha256'] == m['preCorrectionSha256'] == prior['cards'][cid], cid
        for name in ['card-source-bindings.json', 'card-corrections.json']:
            overrides = json.loads((R / 'scripts/markbank' / name).read_text()).get('construction-studies', {})
            assert not [k for k in overrides if k.startswith(PREFIX)], name
    elif integrated is False:  # before integration (None skips authored checks)
        assert all(construction_corrections.card_hash(by_id[cid]) == old_hash for cid, old_hash in
                   [(c, construction_corrections.card_hash(legacy[c])) for c in legacy])
    gaps = {}
    for g in d['taxonomyGaps']:
        assert g['atlasTopicId'] in bindings[g['cardId'].removeprefix(PREFIX)]['atlasTopicIds'] and g['reason'].strip()
        gaps.setdefault(g['cardId'].removeprefix(PREFIX), set()).update(g['canonicalTopicIds'])
    assert gaps == GAPS
    assert d['questionsReviewed'] == list('123456789') and d['unreviewedQuestions'] == []
    return dict(tasks=30, addedTasks=11, correctedTasks=19, consolidatedLegacy=8, leafTasks=len(LEAF),
                wholeQuestions=sum(1 for k in cards if '-complete' in k or k == Q8), q8AnyFiveOfNine=True, sourceFigures=30, paperComplete=True)


if __name__ == '__main__':
    print(json.dumps(validate(json.loads(REVIEW.read_text()))))
