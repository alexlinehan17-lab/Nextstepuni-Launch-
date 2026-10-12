"""Source-pinned validator for the 2026 Ordinary Level Construction Studies theory paper (Q1-Q9).

Checks the reviewed authoring file against the original SEC paper and marking scheme
(byte-identical paper-trail-corpus copies, pinned by SHA-256): page text, lifted
question wording (narrowing only deletes printed words), scheme-traceable rows,
the published tariffs and mark steps, the Q8 choice as ONE any-five card over all nine printed
terms (choice is not a route: no per-term or per-combination cards),
the required pair in Q6(a), pixel-exact figure crops, the selection ledger and exact
topic/Atlas bindings.
"""
import copy
import hashlib
import json
import re
from pathlib import Path

import fitz
from PIL import Image, ImageChops

import construction_corrections

R = Path(__file__).resolve().parents[3]
REVIEW = R / 'scripts/markbank/authored/construction-studies-2026-ordinary-reviewed.json'
FIGURE_DIR = R / 'public/exam-figures/construction-studies/markbank'
P = 'paper-trail-corpus/exampapers/2026/LC029GLP000EV.pdf'
S = 'paper-trail-corpus/markingschemes/2026/LC029GLP000EV.pdf'
HASHES = {P: '3c68a9431babde5a5ba814a72fdd790ffbe44fbc3e00444dc37867e20a3003c6',
          S: '4d5b0f5d024e248e2d1398ceb6641d3800f1c880bf01a1327977d648637a0011'}
PREFIX = 'cons-2026-ol-'
FP = 'construction-studies-2026-OL-'
CROSS = 'construction-studies-ordinary-'
BAND8 = [0, 4, 6, 8]
TERM_ITEMS = ['triple glazing', 'wind turbine', 'carbon monoxide alarm', 'mortise and tenon joint', 'butt hinge',
              'ball valve', 'cordless circular saw', 'fascia board', 'smart meter']
TERM_HEADINGS = ['Triple glazing', 'Wind turbine', 'Carbon monoxide alarm', 'Mortise and tenon joint', 'Butt hinge', 'Ball valve',
                 'Cordless circular saw', 'Fascia board', 'Smart meter']
PRIOR_COUNT = 852


def r(n):
    return list(range(n + 1))


LEAF = {
    'q1-a': [('details', 35, list(range(0, 36, 5))), ('dimensions', 3, r(3)), ('presentation', 8, BAND8)],
    'q1-b': [('damp-prevention', 4, [0, 4])],
    'q2-a': [('advantage-1', 6, r(6)), ('advantage-2', 6, r(6))],
    'q2-b': [('method', 16, r(16)), ('type', 4, r(4)), ('thickness', 4, r(4))],
    'q2-c': [('area', 2, r(2)), ('reason-1', 6, r(6)), ('reason-2', 6, r(6))],
    'q3-a': [('details', 40, list(range(0, 41, 5)))],
    'q3-b': [('use-1', 5, r(5)), ('use-2', 5, r(5))],
    'q4-a': [('reason-1', 5, r(5)), ('reason-2', 5, r(5))],
    'q4-b': [(k, 6, r(6)) for k in ['site', 'house', 'entrance', 'driveway', 'garage']],
    'q4-c': [('item-1', 5, r(5)), ('item-2', 5, r(5))],
    'q5-a': [('details', 35, list(range(0, 36, 5))), ('dimensions', 3, r(3)), ('presentation', 8, BAND8)],
    'q5-b': [('wall-tie', 4, [0, 4])],
    'q6-a-scroll-saw': [('precaution-1', 4, r(4)), ('precaution-2', 4, r(4))],
    'q6-a-spray-finish': [('precaution-1', 4, r(4)), ('precaution-2', 4, r(4))],
    'q6-b': [(f'precaution-{i}', 8, r(8)) for i in (1, 2, 3)],
    'q6-c': [('reason-1', 5, r(5)), ('reason-2', 5, r(5))],
    'q7-a': [('way-1', 5, r(5)), ('way-2', 5, r(5))],
    'q7-b': [('sketch', 8, r(8))] + [(k, 5, r(5)) for k in ['outdoor-living', 'cooking', 'play', 'planting']],
    'q7-c': [('benefit-1', 6, r(6)), ('benefit-2', 6, r(6))],
    'q8': [('terms', 50, None)],
    'q9-a': [('reason-1', 6, r(6)), ('reason-2', 6, r(6))],
    'q9-b': [('modification-1', 13, r(13)), ('modification-2', 13, r(13))],
    'q9-c': [('timber', 4, r(4)), ('reason-1', 4, r(4)), ('reason-2', 4, r(4))],
}
COMPOSITE = {
    'q1-complete': ['q1-a', 'q1-b'], 'q2-complete': ['q2-a', 'q2-b', 'q2-c'], 'q3-complete': ['q3-a', 'q3-b'],
    'q4-complete': ['q4-a', 'q4-b', 'q4-c'], 'q5-complete': ['q5-a', 'q5-b'],
    'q6-a': ['q6-a-scroll-saw', 'q6-a-spray-finish'], 'q6-complete': ['q6-a', 'q6-b', 'q6-c'],
    'q7-complete': ['q7-a', 'q7-b', 'q7-c'],
    'q9-complete': ['q9-a', 'q9-b', 'q9-c'],
}
TOTALS = {'q1-a': 46, 'q1-b': 4, 'q2-a': 12, 'q2-b': 24, 'q2-c': 14, 'q3-a': 40, 'q3-b': 10, 'q4-a': 10, 'q4-b': 30,
          'q4-c': 10, 'q5-a': 46, 'q5-b': 4, 'q6-a': 16, 'q6-a-scroll-saw': 8, 'q6-a-spray-finish': 8, 'q6-b': 24,
          'q6-c': 10, 'q7-a': 10, 'q7-b': 28, 'q7-c': 12, 'q9-a': 12, 'q9-b': 26, 'q9-c': 12,
          'q8': 50, **{k: 50 for k in COMPOSITE if '-complete' in k}}
SCHEME_PAGES = {'1': [4, 18], '2': [5, 19], '3': [6, 20], '4': [7, 8, 21], '5': [9, 22], '6': [10, 11, 23],
                '7': [12, 13, 24], '9': [17, 26]}
PAPER_PAGE = {'1': 2, '2': 2, '3': 2, '4': 3, '5': 3, '6': 3, '7': 4, '8': 4, '9': 4}
PAGE = [48, 52, 568, 790]
FIGURES = {
    'q1-original': (P, 2, [45, 38, 580, 282], False), 'q2-original': (P, 2, [45, 282, 580, 524], False),
    'q3-original': (P, 2, [45, 524, 580, 784], False), 'q4-original': (P, 3, [45, 36, 580, 310], False),
    'q5-original': (P, 3, [45, 310, 580, 552], False), 'q6-original': (P, 3, [45, 552, 580, 785], False),
    'q7-original': (P, 4, [45, 38, 580, 346], False), 'q8-original': (P, 4, [45, 346, 580, 480], False),
    'q9-original': (P, 4, [45, 480, 580, 785], False),
    'q1-section': (S, 4, [50, 138, 545, 492], True), 'q1-scheme': (S, 4, PAGE, True),
    'q2-scheme': (S, 5, PAGE, True), 'q2-upgrade': (S, 5, [436, 616, 574, 766], True),
    'q3-system': (S, 6, [50, 125, 575, 524], True), 'q3-water-butt': (S, 6, [450, 562, 548, 764], True),
    'q4-site-plan': (S, 7, [84, 398, 545, 752], True), 'q4-site-notice': (S, 8, [410, 540, 568, 786], True),
    'q5-section': (S, 9, [50, 102, 572, 578], True), 'q5-wall-tie': (S, 9, [96, 660, 470, 748], True),
    'q6-precautions': (S, 10, [86, 128, 545, 414], True), 'q6-pillar-drill': (S, 10, [345, 530, 545, 752], True),
    'q7-garden-plan': (S, 12, [145, 347, 486, 790], True),
    'q9-extension': (S, 17, [213, 288, 577, 532], True), 'q9-cladding': (S, 17, [433, 557, 546, 780], True),
}
SOLUTION = {'q1-a': 'q1-scheme', 'q1-b': 'q1-section', 'q1-complete': 'q1-scheme', 'q2-b': 'q2-scheme', 'q2-c': 'q2-upgrade',
            'q2-complete': 'q2-scheme', 'q3-a': 'q3-system', 'q3-b': 'q3-water-butt', 'q3-complete': 'q3-system',
            'q4-b': 'q4-site-plan', 'q4-c': 'q4-site-notice', 'q4-complete': 'q4-site-plan', 'q5-a': 'q5-section',
            'q5-b': 'q5-wall-tie', 'q5-complete': 'q5-section', 'q6-a-scroll-saw': 'q6-precautions',
            'q6-a-spray-finish': 'q6-precautions', 'q6-a': 'q6-precautions', 'q6-b': 'q6-pillar-drill',
            'q6-complete': 'q6-precautions', 'q7-b': 'q7-garden-plan', 'q7-complete': 'q7-garden-plan',
            'q9-b': 'q9-extension', 'q9-c': 'q9-cladding', 'q9-complete': 'q9-extension'}
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-2-4', 'cons-3-3', 'cons-4-2', 'cons-3-4', 'cons-6-2'], ['question-one-drawing-questions', 'foundations-floors-walls', 'heat-loss-insulation']),
    'q1-b': (['cons-3-4', 'cons-4-2'], ['foundations-floors-walls']),
    'q2-a': (['cons-6-2', 'cons-6-3'], ['heat-loss-insulation']),
    'q2-b': (['cons-6-2', 'cons-3-3'], ['heat-loss-insulation', 'foundations-floors-walls']),
    'q2-c': (['cons-6-2', 'cons-6-3'], ['heat-loss-insulation']),
    'q3-a': (['cons-5-2', 'cons-5-1'], ['services-water-gas-electrical']), 'q3-b': (['cons-5-4'], ['drainage']),
    'q4-a': (['cons-1-3'], ['planning-sustainability-environment']), 'q4-b': (['cons-1-3'], ['planning-sustainability-environment']),
    'q4-c': (['cons-1-3'], ['planning-sustainability-environment']),
    'q5-a': (['cons-3-7', 'cons-3-3', 'cons-3-4', 'cons-6-2'], ['windows-doors', 'foundations-floors-walls', 'heat-loss-insulation']),
    'q5-b': (['cons-3-3'], ['foundations-floors-walls']),
    'q6-a-scroll-saw': (['cons-9-4'], ['site-safety']), 'q6-a-spray-finish': (['cons-9-4'], ['site-safety']),
    'q6-b': (['cons-9-4'], ['site-safety']), 'q6-c': (['cons-9-4'], ['site-safety']),
    'q7-a': (['cons-1-2'], ['planning-sustainability-environment']), 'q7-b': (['cons-1-2'], ['planning-sustainability-environment']),
    'q7-c': (['cons-6-4', 'cons-1-2'], ['planning-sustainability-environment']),
    'q8': (['cons-3-6', 'cons-6-2', 'cons-1-2', 'cons-1-9', 'cons-5-7', 'cons-10-1', 'cons-10-4', 'cons-4-5', 'cons-3-7', 'cons-5-2', 'cons-9-2', 'cons-9-4', 'cons-3-10', 'cons-5-8'],
           ['windows-doors', 'heat-loss-insulation', 'planning-sustainability-environment', 'fire-places-fire-prevention', 'wood-rot-ventilation', 'services-water-gas-electrical', 'site-safety', 'roofs']),
    'q9-a': (['cons-1-2'], ['planning-sustainability-environment']), 'q9-b': (['cons-3-5', 'cons-3-7'], ['windows-doors']),
    'q9-c': (['cons-3-2', 'cons-10-3'], ['foundations-floors-walls', 'wood-rot-ventilation']),
}
GAPS = {'q8': {'cons-10-1', 'cons-10-4', 'cons-9-2'}}


def tokens(text):
    return re.findall(r'[a-z0-9]+', text.lower())


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
        body += text[text.index('suitable cladding material.') + len('suitable cladding material.'):]
    return body


def validate(d, images=True, figure_dir=FIGURE_DIR, integrated=True):
    assert d['sourceHashes'] == HASHES
    for f, h in HASHES.items():
        assert hashlib.sha256((R / f).read_bytes()).hexdigest() == h, f
    assert (d['subjectId'], d['year'], d['level'], d['lang'], d['sitting'], d['paperKey'], d['fileid']) == (
        'construction-studies', 2026, 'ordinary', 'ev', 'main', 'single', 'LC029GLP000EV.pdf')
    cards = {t['card']['id'].removeprefix(PREFIX): t['card'] for t in d['tasks']}
    tasks = {t['card']['id'].removeprefix(PREFIX): t for t in d['tasks']}
    expected = set(LEAF) | set(COMPOSITE)
    assert set(cards) == expected and len(d['tasks']) == len(expected) == 32
    assert d['addedIds'] == [t['card']['id'] for t in d['tasks']]
    assert len({c['questionRef'] for c in cards.values()}) == 32
    bindings = {b['cardId'].removeprefix(PREFIX): b for b in d['bindings']}
    assert set(bindings) == expected and len(d['bindings']) == 32
    scheme = normalise(' '.join(page_text(S, p) for p in range(1, 27)))
    crosswalk = json.loads((R / 'data/examTopics/construction-studies-curriculum-crosswalk.json').read_text())
    registry = set(re.findall(r"id: '(cons-\d+-\d+)'", (R / 'curriculumRegistry.ts').read_text()))
    library_nodes = {n for nodes in crosswalk.values() for n in nodes}
    figures = {f['key'].removeprefix(FP): f for f in d['questionFigures']}
    assert set(figures) == set(FIGURES) and len(d['questionFigures']) == 24

    for key, c in cards.items():
        q = key[1]
        t, b = tasks[key], bindings[key]
        assert t['questionNumber'] == b['questionNumber'] == q
        assert (c['subjectId'], c['year'], c['level'], c['section']) == ('construction-studies', 2026, 'ordinary', 'B')
        assert c['tariffModel'] == {'kind': 'fixed'} and c['questionRef'].startswith(f'2026 OL Q{q}')
        assert c['questionFigureKey'] == f'{FP}q{q}-original' and c['questionFigureIncludesPrompt'] is True
        assert c['sourceMaterial']['pages'] == [1, PAPER_PAGE[q]] and t['requiredQuestionFigures'] == [c['questionFigureKey']]
        assert c.get('figureKey') == (FP + SOLUTION[key] if key in SOLUTION else None), key
        assert t['requiredSolutionFigures'] == ([FP + SOLUTION[key]] if key in SOLUTION else [])
        if key in SOLUTION:
            assert figures[SOLUTION[key]]['solution'] is True
        assert figures[f'q{q}-original']['solution'] is False
        words = tokens(region(q))
        assert is_subsequence(tokens(c['questionText']), words), (key, 'questionText not lifted')
        assert is_subsequence(tokens(c['stem']), words), (key, 'stem not lifted')
        for row in c['rows']:
            assert row['contextNote'].strip()
            if row['kind'] == 'anyN':  # a closed choice: every printed option, in the scheme's own headings
                assert 'permittedMarks' not in row and row['marks'] == row['group']['claimMax'] * row['group']['perOption'], (key, row['id'])
                assert all(normalise(o) in scheme for o in row['group']['options']), (key, 'option not printed in the scheme')
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
        pages = [14, 15, 16, 25] if q == '8' else SCHEME_PAGES[q]
        assert [(x['file'], x['page']) for x in t['sourceChecks']] == [(P, 1), (P, PAPER_PAGE[q])] + [(S, p) for p in [2, 3, *pages]], key
        for x in t['sourceChecks']:
            assert hashlib.sha256(page_text(x['file'], x['page']).encode()).hexdigest() == x['textSha256'], (key, x)

    # Choice is not a route: Q8 is ONE card printing all nine terms, with one any-five group over them.
    q8 = cards['q8']
    assert [k for k in cards if k.startswith('q8')] == ['q8'] and 'taskGroups' not in q8
    assert q8['questionText'].endswith('any five of the following: ' + '; '.join(TERM_ITEMS) + '.')
    assert q8['rows'][0]['kind'] == 'anyN' and q8['rows'][0]['group'] == dict(claimMax=5, perOption=10, options=TERM_HEADINGS)
    sel = d['selectionLedger']
    assert sel['finiteQuestionChoices']['8']['cardId'] == PREFIX + 'q8' and 'routes' not in sel['finiteQuestionChoices']['8']
    assert sel['unclassified'] == 0 and all(x['classification'] for x in sel['rows'])
    observed = []
    with fitz.open(R / P) as pdf:
        for i, p in enumerate(pdf):
            observed.extend((i + 1, m.start(), m.group()) for m in re.finditer(sel['pattern'], ' '.join(p.get_text().split()), re.I))
    assert observed == [(x['page'], x['start'], x['match']) for x in sel['rows']] and len(observed) == 2
    for q in '123456789':
        whole = ['q8'] if q == '8' else [k for k in cards if k.startswith(f'q{q}-complete')]
        assert whole and {w['id'] for w in d['questionRouteLedgers'][q]['wholeRoutes']} == {PREFIX + k for k in whole}

    for key, f in figures.items():
        assert (f['source'], f['page'], f['rect'], f['solution']) == FIGURES[key] and f['visuallyInspected'] and f['renderScale'] == 2
        path = Path(figure_dir) / f"{f['key']}.png"
        assert hashlib.sha256(path.read_bytes()).hexdigest() == f['sha256'], key
        if images:
            with fitz.open(R / f['source']) as pdf:
                px = pdf[f['page'] - 1].get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(f['rect']), alpha=False)
            a = Image.frombytes('RGB', (px.width, px.height), px.samples)
            saved = Image.open(path).convert('RGB')
            assert a.size == saved.size and ImageChops.difference(a, saved).getbbox() is None, key
    assert len({f['sha256'] for f in d['questionFigures']}) == 24

    if integrated:
        prior = json.loads((R / 'docs/markbank-audit/2026-09-28/drafts/construction-2026-ordinary/prior-authored-card-hashes.json').read_text())
        authored = json.loads((R / 'scripts/markbank/authored/construction-studies.json').read_text())
        by_id = {c['id']: c for c in authored}
        assert prior['count'] == len(prior['cards']) == PRIOR_COUNT and len(by_id) == len(authored)
        # Byte-identical, or replaced in place through a later review's recorded, hash-linked correction.
        construction_corrections.assert_prior_cards_preserved(prior['cards'], by_id)
        assert all(by_id[t['card']['id']] == t['card'] for t in d['tasks'])
    gaps = {g['cardId'].removeprefix(PREFIX): set(g['canonicalTopicIds']) for g in d['taxonomyGaps']}
    assert gaps == GAPS
    assert d['questionsReviewed'] == list('123456789') and d['unreviewedQuestions'] == []
    return dict(tasks=32, leafTasks=len(LEAF), wholeQuestions=sum(1 for k in cards if '-complete' in k or k == 'q8'),
                q8AnyFiveOfNine=True, sourceFigures=24, paperComplete=True)


if __name__ == '__main__':
    print(json.dumps(validate(json.loads(REVIEW.read_text()))))
