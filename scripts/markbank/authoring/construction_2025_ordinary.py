"""Source-pinned validator for the 2025 Ordinary Level Construction Studies theory paper (Q1-Q9).

Checks the reviewed authoring file against the original SEC paper and marking scheme
(byte-identical paper-trail-corpus copies, pinned by SHA-256): page text, lifted question
wording (narrowing only deletes printed words), scheme-traceable rows, the published tariffs
and mark steps, the Q8 choice as ONE any-five card over all nine printed terms (choice is not a
route: no per-term or per-combination cards), the required PPE items in Q6(a),
pixel-exact figure crops, the selection ledger and exact topic/Atlas bindings. The 21 pre-audit
2025 Ordinary cards keep their IDs and concept IDs and are corrected in place; each correction is
hash-linked to the card it replaced, and every other prior card stays byte-identical.
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
REVIEW = R / 'scripts/markbank/authored/construction-studies-2025-ordinary-reviewed.json'
DRAFTS = R / 'docs/markbank-audit/2026-09-28/drafts/construction-2025-ordinary'
FIGURE_DIR = R / 'public/exam-figures/construction-studies/markbank'
P = 'paper-trail-corpus/exampapers/2025/LC029GLP000EV.pdf'
S = 'paper-trail-corpus/markingschemes/2025/LC029GLP000EV.pdf'
HASHES = {P: '6aca987b0c66e490252998240bde8e2ca6f30f992a425db364bb2ec643b2fa4d',
          S: 'ea1b7818d3caac4ff8e7b712e4abe3899245c7051ba66520d6ff81c9ca5612d9'}
PREFIX = 'cons-2025-ol-'
FP = 'construction-studies-2025-OL-'
CROSS = 'construction-studies-ordinary-'
BAND8 = [0, 4, 6, 8]
BAND5 = [0, 1, 3, 5]
TERM_ITEMS = ['raft foundation', 'housing joint', 'rainwater butt', 'stud wall', 'laser level', 'damp-proof course',
              'door threshold', 'baluster', 'room thermostat']
TERM_HEADINGS = ['Raft foundation', 'Housing joint', 'Rainwater butt', 'Stud wall', 'Laser level', 'Damp-proof course',
                 'Door threshold', 'Baluster', 'Room thermostat']
PPE = ['high-visibility-vest', 'safety-boots', 'ear-defenders']
PRIOR_COUNT = 1070
LEGACY = {'q1-a', 'q1-b', 'q2-a', 'q2-b', 'q2-c', 'q3-a', 'q3-b', 'q4-a', 'q4-b', 'q4-c', 'q5-a', 'q5-b', 'q6-a', 'q6-b',
          'q6-c', 'q7-a', 'q7-b', 'q7-c-advantage', 'q7-c-disadvantage', 'q9-b', 'q9-c'}


def r(n):
    return list(range(n + 1))


LEAF = {
    'q1-a': [('details', 35, list(range(0, 36, 5))), ('dimensions', 3, r(3)), ('presentation', 8, BAND8)],
    'q1-b': [('stepped-dpc', 4, [0, 4])],
    'q2-a': [('advantage-1', 6, r(6)), ('advantage-2', 6, r(6))],
    'q2-b': [('method', 16, r(16)), ('type', 4, r(4)), ('thickness', 4, r(4))],
    'q2-c': [('note', 7, r(7)), ('sketch', 7, r(7))],
    'q3-a': [('details', 40, list(range(0, 41, 5))), ('quality', 5, BAND5)],
    'q3-b': [('advantage', 5, r(5))],
    'q4-a': [('select', 2, r(2)), ('reason-1', 6, r(6)), ('reason-2', 6, r(6))],
    'q4-b': [(k, 6, r(6)) for k in ['site', 'house', 'entrance', 'driveway']],
    'q4-c': [('advantage', 6, r(6)), ('disadvantage', 6, r(6))],
    'q5-a': [('details', 35, list(range(0, 36, 5))), ('dimensions', 3, r(3)), ('presentation', 8, BAND8)],
    'q5-b': [('glue-blocks', 4, [0, 4])],
    **{f'q6-a-{p}': [('sign-reason', 8, r(8))] for p in PPE},
    'q6-b': [('risk-1', 6, r(6)), ('risk-2', 6, r(6))],
    'q6-c': [('notes', 7, r(7)), ('sketch', 7, r(7))],
    'q7-a': [('advantage-1', 5, r(5)), ('advantage-2', 5, r(5))],
    'q7-b': [('sketch', 8, BAND8)] + [(k, 5, r(5)) for k in ['corner-desk', 'two-windows', 'bookcase', 'seating']],
    'q7-c-advantage': [('advantage', 6, r(6))], 'q7-c-disadvantage': [('disadvantage', 6, r(6))],
    'q8': [('terms', 50, None)],
    'q9-a': [('reason-1', 6, r(6)), ('reason-2', 6, r(6))],
    'q9-b': [('modification-1', 13, r(13)), ('modification-2', 13, r(13))],
    'q9-c': [('use-1', 6, r(6)), ('use-2', 6, r(6))],
}
COMPOSITE = {
    'q1-complete': ['q1-a', 'q1-b'], 'q2-complete': ['q2-a', 'q2-b', 'q2-c'], 'q3-complete': ['q3-a', 'q3-b'],
    'q4-complete': ['q4-a', 'q4-b', 'q4-c'], 'q5-complete': ['q5-a', 'q5-b'],
    'q6-a': [f'q6-a-{p}' for p in PPE], 'q6-complete': ['q6-a', 'q6-b', 'q6-c'],
    'q7-c': ['q7-c-advantage', 'q7-c-disadvantage'], 'q7-complete': ['q7-a', 'q7-b', 'q7-c'],
    'q9-complete': ['q9-a', 'q9-b', 'q9-c'],
}
TOTALS = {'q1-a': 46, 'q1-b': 4, 'q2-a': 12, 'q2-b': 24, 'q2-c': 14, 'q3-a': 45, 'q3-b': 5, 'q4-a': 14, 'q4-b': 24,
          'q4-c': 12, 'q5-a': 46, 'q5-b': 4, 'q6-a': 24, **{f'q6-a-{p}': 8 for p in PPE}, 'q6-b': 12, 'q6-c': 14,
          'q7-a': 10, 'q7-b': 28, 'q7-c': 12, 'q7-c-advantage': 6, 'q7-c-disadvantage': 6, 'q9-a': 12, 'q9-b': 26, 'q9-c': 12,
          'q8': 50, **{k: 50 for k in COMPOSITE if '-complete' in k}}
SCHEME_PAGES = {'1': [4, 17], '2': [5, 18], '3': [6, 19], '4': [7, 8, 20], '5': [9, 21], '6': [10, 22],
                '7': [11, 12, 23], '9': [16, 25]}
PAPER_PAGE = {'1': 2, '2': 2, '3': 2, '4': 3, '5': 3, '6': 3, '7': 4, '8': 4, '9': 4}
PAGE = [48, 46, 578, 800]
FIGURES = {
    'q1-original': (P, 2, [45, 40, 580, 262], False), 'q2-original': (P, 2, [45, 280, 580, 500], False),
    'q3-original': (P, 2, [45, 515, 580, 775], False), 'q4-original': (P, 3, [45, 40, 580, 290], False),
    'q5-original': (P, 3, [45, 300, 580, 510], False), 'q6-original': (P, 3, [45, 520, 580, 772], False),
    'q7-original': (P, 4, [45, 50, 580, 368], False), 'q8-original': (P, 4, [45, 380, 580, 482], False),
    'q9-original': (P, 4, [45, 495, 580, 770], False),
    'q1-scheme': (S, 4, PAGE, True), 'q1-section': (S, 4, [80, 108, 480, 568], True),
    'q2-method': (S, 5, [48, 222, 578, 654], True), 'q2-light': (S, 5, [48, 655, 578, 790], True),
    'q3-system': (S, 6, [30, 118, 560, 570], True), 'q3-zoning': (S, 6, [48, 598, 578, 790], True),
    'q4-sites': (S, 7, [48, 100, 578, 420], True), 'q4-site-a': (S, 7, [48, 425, 578, 790], True),
    'q5-section': (S, 9, [48, 84, 578, 575], True), 'q5-glue-blocks': (S, 9, [48, 580, 578, 790], True),
    'q6-signs': (S, 10, [48, 84, 578, 352], True), 'q6-risks': (S, 10, [48, 356, 578, 530], True),
    'q6-access': (S, 10, [48, 540, 578, 795], True), 'q7-office-plan': (S, 11, [48, 290, 578, 790], True),
    'q9-modifications': (S, 16, [48, 243, 578, 535], True), 'q9-uses': (S, 16, [48, 547, 578, 790], True),
}
SOLUTION = {'q1-a': 'q1-scheme', 'q1-b': 'q1-section', 'q1-complete': 'q1-scheme', 'q2-b': 'q2-method', 'q2-c': 'q2-light',
            'q2-complete': 'q2-method', 'q3-a': 'q3-system', 'q3-b': 'q3-zoning', 'q3-complete': 'q3-system',
            'q4-a': 'q4-sites', 'q4-b': 'q4-site-a', 'q4-complete': 'q4-site-a', 'q5-a': 'q5-section',
            'q5-b': 'q5-glue-blocks', 'q5-complete': 'q5-section', **{f'q6-a-{p}': 'q6-signs' for p in PPE},
            'q6-a': 'q6-signs', 'q6-b': 'q6-risks', 'q6-c': 'q6-access', 'q6-complete': 'q6-signs',
            'q7-b': 'q7-office-plan', 'q7-complete': 'q7-office-plan',
            'q9-b': 'q9-modifications', 'q9-c': 'q9-uses', 'q9-complete': 'q9-modifications'}
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-3-3', 'cons-3-4', 'cons-3-6', 'cons-6-2'], ['question-one-drawing-questions', 'foundations-floors-walls', 'windows-doors', 'heat-loss-insulation']),
    'q1-b': (['cons-3-4', 'cons-3-6'], ['foundations-floors-walls', 'windows-doors']),
    'q2-a': (['cons-6-2', 'cons-6-3'], ['heat-loss-insulation']),
    'q2-b': (['cons-3-9', 'cons-6-2'], ['roofs', 'heat-loss-insulation']),
    'q2-c': (['cons-3-5', 'cons-3-9'], ['windows-doors', 'roofs']),
    'q3-a': (['cons-5-3', 'cons-5-2'], ['hot-water-space-heating']), 'q3-b': (['cons-5-3'], ['hot-water-space-heating']),
    **{f'q4-{p}': (['cons-1-3'], ['planning-sustainability-environment']) for p in 'abc'},
    'q5-a': (['cons-1-5', 'cons-4-4', 'cons-4-3', 'cons-10-1'], ['question-one-drawing-questions', 'foundations-floors-walls', 'wood-rot-ventilation']),
    'q5-b': (['cons-4-4', 'cons-10-1'], ['wood-rot-ventilation']),
    **{f'q6-a-{p}': (['cons-1-8'], ['site-safety']) for p in PPE},
    'q6-b': (['cons-1-8'], ['site-safety']), 'q6-c': (['cons-1-8'], ['site-safety']),
    'q7-a': (['cons-3-3', 'cons-1-2'], ['foundations-floors-walls', 'planning-sustainability-environment']),
    'q7-b': (['cons-1-2'], ['planning-sustainability-environment']),
    'q7-c-advantage': (['cons-1-2'], ['planning-sustainability-environment']),
    'q7-c-disadvantage': (['cons-1-2'], ['planning-sustainability-environment']),
    'q8': (['cons-2-4', 'cons-2-2', 'cons-10-1', 'cons-10-4', 'cons-5-4', 'cons-4-5', 'cons-10-7', 'cons-9-2', 'cons-3-4', 'cons-3-7', 'cons-4-4', 'cons-5-3'],
           ['foundations-floors-walls', 'wood-rot-ventilation', 'drainage', 'windows-doors', 'hot-water-space-heating']),
    'q9-a': (['cons-1-2'], ['planning-sustainability-environment']),
    'q9-b': (['cons-3-7', 'cons-1-2'], ['windows-doors', 'planning-sustainability-environment']),
    'q9-c': (['cons-1-2'], ['planning-sustainability-environment']),
}
GAPS = {'q5-a': {'cons-4-4', 'cons-10-1'}, 'q5-b': {'cons-4-4', 'cons-10-1'}, 'q8': {'cons-10-1', 'cons-10-4', 'cons-9-2', 'cons-4-4'}}


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
        body += text[text.index('uses of a large garden.') + len('uses of a large garden.'):]
    return body


def validate(d, images=True, figure_dir=FIGURE_DIR, integrated=True):
    assert d['sourceHashes'] == HASHES
    for f, h in HASHES.items():
        assert hashlib.sha256((R / f).read_bytes()).hexdigest() == h, f
    assert (d['subjectId'], d['year'], d['level'], d['lang'], d['sitting'], d['paperKey'], d['fileid']) == (
        'construction-studies', 2025, 'ordinary', 'ev', 'main', 'single', 'LC029GLP000EV.pdf')
    cards = {t['card']['id'].removeprefix(PREFIX): t['card'] for t in d['tasks']}
    tasks = {t['card']['id'].removeprefix(PREFIX): t for t in d['tasks']}
    expected = set(LEAF) | set(COMPOSITE)
    assert set(cards) == expected and len(d['tasks']) == len(expected) == 35
    assert d['addedIds'] == [t['card']['id'] for t in d['tasks'] if t['card']['id'].removeprefix(PREFIX) not in LEGACY]
    assert len(d['addedIds']) == 14 and all(t['correction'] == (k in LEGACY) for k, t in tasks.items())
    assert len({c['questionRef'] for c in cards.values()}) == 35
    bindings = {b['cardId'].removeprefix(PREFIX): b for b in d['bindings']}
    assert set(bindings) == expected and len(d['bindings']) == 35
    scheme = normalise(' '.join(page_text(S, p) for p in range(1, 26)))
    crosswalk = json.loads((R / 'data/examTopics/construction-studies-curriculum-crosswalk.json').read_text())
    registry = set(re.findall(r"id: '(cons-\d+-\d+)'", (R / 'curriculumRegistry.ts').read_text()))
    library_nodes = {n for nodes in crosswalk.values() for n in nodes}
    figures = {f['key'].removeprefix(FP): f for f in d['questionFigures']}
    assert set(figures) == set(FIGURES) and len(d['questionFigures']) == 25

    for key, c in cards.items():
        q = key[1]
        t, b = tasks[key], bindings[key]
        assert t['questionNumber'] == b['questionNumber'] == q
        assert (c['subjectId'], c['year'], c['level'], c['section']) == ('construction-studies', 2025, 'ordinary', 'B')
        assert c['tariffModel'] == {'kind': 'fixed'} and c['questionRef'].startswith(f'2025 OL Q{q}')
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
        pages = [13, 14, 15, 24] if q == '8' else SCHEME_PAGES[q]
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
    assert observed == [(x['page'], x['start'], x['match']) for x in sel['rows']] and len(observed) == 4
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
    assert len({f['sha256'] for f in d['questionFigures']}) == 25

    # In-place corrections: same ID and concept ID, hash-linked to the pre-audit card they replace.
    legacy = {c['id']: c for c in json.loads((DRAFTS / 'prior-2025-ordinary-cards.json').read_text())}
    assert set(legacy) == {PREFIX + k for k in LEGACY}
    fixes = {x['cardId']: x for x in d['corrections']}
    assert set(fixes) == set(legacy) and len(d['corrections']) == 21
    for cid, old in legacy.items():
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
        for cid in legacy:
            assert prior['cards'][cid] == fixes[cid]['priorSha256'], cid
        construction_corrections.assert_prior_cards_preserved(prior['cards'], by_id)
        assert all(by_id[t['card']['id']] == t['card'] for t in d['tasks'])
        # No build-time override may replace reviewed content.
        for name in ['card-source-bindings.json', 'card-corrections.json']:
            overrides = json.loads((R / 'scripts/markbank' / name).read_text()).get('construction-studies', {})
            assert not [k for k in overrides if k.startswith(PREFIX)], name
        assert [x['cardId'] for x in d.get('retiredBuildOverrides', [])] == [PREFIX + 'q7-c-advantage']
    elif integrated is False:  # before integration (None skips authored checks, for a consolidation)
        assert all(construction_corrections.card_hash(by_id[cid]) == fixes[cid]['priorSha256'] for cid in legacy)
    gaps = {g['cardId'].removeprefix(PREFIX): set(g['canonicalTopicIds']) for g in d['taxonomyGaps']}
    assert gaps == GAPS
    assert d['questionsReviewed'] == list('123456789') and d['unreviewedQuestions'] == []
    return dict(tasks=35, addedTasks=14, correctedTasks=21, leafTasks=len(LEAF),
                wholeQuestions=sum(1 for k in cards if '-complete' in k or k == 'q8'), q8AnyFiveOfNine=True, sourceFigures=25, paperComplete=True)


if __name__ == '__main__':
    print(json.dumps(validate(json.loads(REVIEW.read_text()))))
