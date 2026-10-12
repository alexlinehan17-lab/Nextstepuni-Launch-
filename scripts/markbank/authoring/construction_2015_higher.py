"""Source-pinned validator for the 2015 Higher Level Construction Studies theory paper (Q1-Q10 and the Q10 alternative).

Checks the reviewed authoring file against the original SEC paper and marking scheme: pinned hashes
and page text, lifted wording (narrowing only deletes printed words; a task named by reference to a
printed list carries the scheme's own heading after ' — '), scheme-traceable rows, the published
tariffs and steps, every printed choice as ONE card with an anyN group over all its items (Q4(a),
Q4(b), Q6(b), Q9(a), Q10(a): choice is not a route) and Q3(b) as one task marked alike for either
option, the separate alternative Q10, pixel-exact figure crops (single rects and 2x panel
composites), the selection ledger and exact topic/Atlas bindings.

The earlier 2015 Higher review was branch-only (never on main). Of its 102 tasks, 37 keep their IDs
and are corrected in place (hash-linked to the card each replaced); the other 65 per-item,
per-combination and per-option route tasks are withdrawn through recorded, hash-linked withdrawals.
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
REVIEW = R / 'scripts/markbank/authored/construction-studies-2015-higher-reviewed.json'
DRAFTS = R / 'docs/markbank-audit/2026-09-28/drafts/construction-2015-higher'
FIGURE_DIR = R / 'public/exam-figures/construction-studies/markbank'
P = 'paper-trail-corpus/exampapers/2015/LC029ALP000EV.pdf'
S = 'paper-trail-corpus/markingschemes/2015/LC029ALP000EV.pdf'
HASHES = {P: '08976c01caaf916102e5f9f0aa18a512a5bf6aa2cad2ce5320208a63970fdc13',
          S: '9558f06c3c50cb7c858d0b4fb299b437277c0efcd182e0811c6aff0bb7dab3ef'}
PREFIX = 'cons-2015-hl-'
FP = 'construction-studies-2015-HL-'
CROSS = 'construction-studies-higher-'
LIGATURES = {'Ɵ': 'ti', 'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬀ': 'ff', 'ﬃ': 'ffi', 'ﬄ': 'ffl'}
ADDED = {'q3-b', 'q3-complete', 'q4-a', 'q4-b', 'q4-complete', 'q6-b', 'q6-complete', 'q9-a', 'q9-complete', 'q10-a', 'q10-complete'}
CHOICES = {'q4-a': ('items', 2, 10, ['Respect for local character', 'Breathable structure', 'Reuse of materials']),
           'q4-b': ('areas', 2, 20, ['Roof', 'Sliding sash windows', 'Suspended timber floor']),
           'q6-b': ('features', 2, 10, ['Compact form', 'Flexible design', 'Low maintenance']),
           'q9-a': ('locations', 3, 16, ['Junction of roof and wall at eaves', 'Junction of upper floors and external walls', 'Window cill',
                                         'Ground floors abutting external walls']),
           'q10-a': ('items', 2, 16, ['Airtight building envelope', 'Space heating demand', 'Indoor air quality'])}


def r(n):
    return list(range(n + 1))


LEAF = {
    'q1-a': [('construction', 44, r(44)), ('presentation', 8, [0, 2, 3, 4, 6, 7, 8])],
    'q1-b': [('access', 8, [0, 8])],
    'q2-a': [('response', 24, list(range(0, 25, 4)))],
    'q2-b': [('response', 24, r(24))],
    'q2-c': [('response', 12, list(range(0, 13, 3)))],
    'q3-a-A': [(k, 3, r(3)) for k in ['advantage-1', 'advantage-2', 'disadvantage-1', 'disadvantage-2']],
    'q3-a-B': [(k, 3, r(3)) for k in ['advantage-1', 'advantage-2', 'disadvantage-1', 'disadvantage-2']],
    'q3-b': [(k, 6, r(6)) for k in ['external-notes', 'external-sketches', 'layout-notes', 'layout-sketches', 'garden-link']],
    'q3-c': [('advantage-1', 3, r(3)), ('advantage-2', 3, r(3))],
    'q4-a': [('items', 20, None)],
    'q4-b': [('areas', 40, None)],
    'q5-a': [('method', 3, [0, 3]), ('resistances', 21, list(range(0, 22, 3))), ('total-resistance', 3, [0, 3]), ('u-value', 3, [0, 1, 3])],
    'q5-b-new': [(k, 2, [0, 2]) for k in ['heat-rate', 'heating-time', 'annual-energy', 'oil', 'annual-cost']],
    'q5-b-existing': [(k, 2, [0, 2]) for k in ['heat-rate', 'heating-time', 'annual-energy', 'oil', 'annual-cost']],
    'q5-c': [('annotations', 5, [0, 5]), ('sketches', 5, [0, 5])],
    'q6-a': [(f'feature-{i}', 10, [0, 5, 10]) for i in (1, 2, 3)],
    'q6-b': [('features', 20, None)],
    'q6-c': [('discussion', 10, [0, 4, 6, 10])],
    'q7-a': [('construction', 40, r(40)), ('dimensions', 4, [0, 4]), ('presentation', 8, [0, 2, 3, 4, 6, 7, 8])],
    'q7-b-eaves': [('eaves', 4, [0, 4])],
    'q7-b-ridge': [('ridge', 4, [0, 4])],
    'q8-a': [('system', 36, r(36)), ('sizes', 4, [0, 2, 4])],
    'q8-b': [('notes', 4, [0, 4]), ('sketch', 4, [0, 4])],
    'q8-c-chimney': [('notes', 3, [0, 3]), ('sketch', 3, [0, 3])],
    'q8-c-hotpress': [('notes', 3, [0, 3]), ('sketch', 3, [0, 3])],
    'q9-a': [('locations', 48, None)],
    'q9-b': [('point-1', 6, [0, 2, 4, 6]), ('point-2', 6, [0, 2, 4, 6])],
    'q10-a': [('items', 32, None)],
    'q10-b': [('notes', 7, [0, 7]), ('sketch', 7, [0, 7])],
    'q10-c': [('notes', 7, [0, 7]), ('sketch', 7, [0, 7])],
    'q10-alt-discussion': [(f'point-{i}', 8, [0, 3, 5, 8]) for i in (1, 2, 3)],
    'q10-alt-glazing': [('advances', 6, [0, 6])],
    'q10-alt-guidelines': [(f'guideline-{i}', 10, [0, 4, 6, 10]) for i in (1, 2, 3)],
}
COMPOSITE = {
    'q1-complete': ['q1-a', 'q1-b'], 'q2-complete': ['q2-a', 'q2-b', 'q2-c'],
    'q3-a': ['q3-a-A', 'q3-a-B'], 'q3-complete': ['q3-a-A', 'q3-a-B', 'q3-b', 'q3-c'],
    'q4-complete': ['q4-a', 'q4-b'],
    'q5-b': ['q5-b-new', 'q5-b-existing'], 'q5-complete': ['q5-a', 'q5-b-new', 'q5-b-existing', 'q5-c'],
    'q6-complete': ['q6-a', 'q6-b', 'q6-c'],
    'q7-b': ['q7-b-eaves', 'q7-b-ridge'], 'q7-complete': ['q7-a', 'q7-b'],
    'q8-c': ['q8-c-chimney', 'q8-c-hotpress'], 'q8-complete': ['q8-a', 'q8-b', 'q8-c'],
    'q9-complete': ['q9-a', 'q9-b'], 'q10-complete': ['q10-a', 'q10-b', 'q10-c'],
    'q10-alt-complete': ['q10-alt-discussion', 'q10-alt-glazing', 'q10-alt-guidelines'],
}
PART_TOTALS = {'q1-a': 52, 'q1-b': 8, 'q2-a': 24, 'q2-b': 24, 'q2-c': 12, 'q3-a-A': 12, 'q3-a-B': 12, 'q3-a': 24, 'q3-b': 30, 'q3-c': 6,
               'q4-a': 20, 'q4-b': 40, 'q5-a': 30, 'q5-b-new': 10, 'q5-b-existing': 10, 'q5-b': 20, 'q5-c': 10,
               'q6-a': 30, 'q6-b': 20, 'q6-c': 10, 'q7-a': 52, 'q7-b-eaves': 4, 'q7-b-ridge': 4, 'q7-b': 8,
               'q8-a': 40, 'q8-b': 8, 'q8-c-chimney': 6, 'q8-c-hotpress': 6, 'q8-c': 12, 'q9-a': 48, 'q9-b': 12,
               'q10-a': 32, 'q10-b': 14, 'q10-c': 14, 'q10-alt-discussion': 24, 'q10-alt-glazing': 6, 'q10-alt-guidelines': 30,
               **{k: 60 for k in COMPOSITE if '-complete' in k}}
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-3-7', 'cons-3-3', 'cons-4-2', 'cons-6-2'], ['question-1-drawing-questions', 'doors', 'walls', 'floors', 'heat-loss-insulation']),
    'q1-b': (['cons-3-7'], ['doors']),
    'q2-a': (['cons-3-2'], ['walls']), 'q2-b': (['cons-3-2', 'cons-3-3'], ['walls']), 'q2-c': (['cons-3-2', 'cons-3-3'], ['walls']),
    'q3-a-A': (['cons-1-2', 'cons-1-3'], ['planning-sustainability-environment']),
    'q3-a-B': (['cons-1-2', 'cons-1-3'], ['planning-sustainability-environment']),
    'q3-b': (['cons-1-3', 'cons-1-2'], ['planning-sustainability-environment']),
    'q3-c': (['cons-1-2'], ['planning-sustainability-environment']),
    'q4-a': (['cons-1-1', 'cons-1-2', 'cons-6-6', 'cons-6-2'], ['conservation-restoration', 'condensation-air-tightness', 'heat-loss-insulation']),
    'q4-b': (['cons-1-1', 'cons-3-8', 'cons-3-9', 'cons-3-5', 'cons-3-6', 'cons-4-2', 'cons-4-3', 'cons-6-2'],
             ['conservation-restoration', 'roofs', 'windows-light', 'floors', 'heat-loss-insulation']),
    'q5-a': (['cons-6-1'], ['heat-u-value-calculations']),
    'q5-b-new': (['cons-6-3'], ['heat-u-value-calculations']), 'q5-b-existing': (['cons-6-3'], ['heat-u-value-calculations']),
    'q5-c': (['cons-3-4', 'cons-3-6'], ['walls', 'windows-light']),
    'q6-a': (['cons-1-2', 'cons-6-2', 'cons-6-4'], ['planning-sustainability-environment', 'passive-design', 'heat-loss-insulation']),
    'q6-b': (['cons-1-2'], ['planning-sustainability-environment']), 'q6-c': (['cons-1-2'], ['planning-sustainability-environment']),
    'q7-a': (['cons-3-8', 'cons-3-9', 'cons-3-3', 'cons-4-3', 'cons-6-2'], ['roofs', 'walls', 'floors', 'heat-loss-insulation']),
    'q7-b-eaves': (['cons-3-9', 'cons-6-5'], ['roofs', 'wood-rot-ventilation']),
    'q7-b-ridge': (['cons-3-9', 'cons-6-5'], ['roofs', 'wood-rot-ventilation']),
    'q8-a': (['cons-5-3', 'cons-5-2'], ['hot-water-space-heating']), 'q8-b': (['cons-5-2', 'cons-5-3'], ['hot-water-space-heating']),
    'q8-c-chimney': (['cons-5-7'], ['fireplaces-fire-prevention']),
    'q8-c-hotpress': (['cons-5-2', 'cons-5-3'], ['hot-water-space-heating']),
    'q9-a': (['cons-6-2', 'cons-3-9', 'cons-3-3', 'cons-4-3', 'cons-3-6', 'cons-4-2'], ['heat-loss-insulation', 'roofs', 'walls', 'floors', 'windows-light']),
    'q9-b': (['cons-6-2', 'cons-6-6'], ['heat-loss-insulation', 'condensation-air-tightness']),
    'q10-a': (['cons-6-5', 'cons-6-6', 'cons-5-3', 'cons-6-2'], ['passive-design', 'condensation-air-tightness', 'hot-water-space-heating', 'wood-rot-ventilation']),
    'q10-b': (['cons-6-4'], ['passive-design']), 'q10-c': (['cons-6-4', 'cons-7-3'], ['passive-design', 'windows-light']),
    'q10-alt-discussion': (['cons-7-4', 'cons-3-5'], ['windows-light']), 'q10-alt-glazing': (['cons-3-6'], ['windows-light']),
    'q10-alt-guidelines': (['cons-7-4', 'cons-3-5', 'cons-1-3'], ['windows-light', 'planning-sustainability-environment']),
}
# key -> (panels [(source, page, rect)], solution); a single-rect crop is one panel stored without a panel list.
SINGLE = {'q1-original': (P, 2, [58, 54, 565, 252], False), 'q1-scheme': (S, 4, [60, 104, 558, 767], True),
          'q1-access-scheme': (S, 5, [27, 460, 573, 627], True), 'q2-original': (P, 2, [58, 267, 565, 421], False),
          'q3-original': (P, 2, [58, 444, 565, 780], False), 'q3-scheme': (S, 10, [54, 52, 577, 793], True),
          'q5-original': (P, 3, [58, 319, 568, 793], False), 'q5-window-head': (S, 17, [54, 33, 573, 315], True),
          'q7-original': (P, 4, [58, 364, 571, 559], False), 'q7-roof-section': (S, 21, [92, 397, 513, 787], True)}
PANELS = {'q4-original': ([(P, 3, [57, 54, 568, 302])], False),
          'q4-roof-windows': ([(S, 12, [54, 242, 568, 768]), (S, 13, [54, 54, 568, 158]), (S, 13, [54, 267, 568, 776]), (S, 14, [54, 54, 573, 792])], True),
          'q6-original': ([(P, 4, [58, 54, 568, 354])], False), 'q6-compact': ([(S, 18, [54, 54, 570, 701])], True),
          'q6-scheme': ([(S, 18, [54, 54, 570, 701]), (S, 19, [54, 54, 574, 450])], True),
          'q8-original': ([(P, 4, [58, 569, 572, 783])], False), 'q8-system': ([(S, 22, [40, 54, 568, 779])], True),
          'q8-collector': ([(S, 22, [40, 54, 568, 779]), (S, 23, [57, 54, 567, 327])], True),
          'q8-locations': ([(S, 23, [55, 333, 568, 779])], True),
          'q8-scheme': ([(S, 22, [40, 54, 568, 779]), (S, 23, [57, 54, 567, 327]), (S, 23, [55, 333, 568, 779])], True),
          'q9-original': ([(P, 5, [58, 49, 566, 288])], False), 'q9-scheme': ([(S, 24, [54, 54, 581, 765]), (S, 25, [54, 54, 568, 262])], True),
          'q10-original': ([(P, 5, [58, 302, 572, 486])], False), 'q10-alternative': ([(P, 5, [58, 560, 572, 771])], False),
          'q10-scheme': ([(S, 25, [54, 264, 570, 776]), (S, 26, [54, 54, 574, 785]), (S, 27, [54, 54, 571, 778]), (S, 28, [43, 54, 575, 786])], True)}
SOLUTION = {'q1-a': 'q1-scheme', 'q1-b': 'q1-access-scheme', 'q1-complete': 'q1-scheme', 'q3-b': 'q3-scheme', 'q3-complete': 'q3-scheme',
            'q4-b': 'q4-roof-windows', 'q4-complete': 'q4-roof-windows', 'q5-c': 'q5-window-head', 'q5-complete': 'q5-window-head',
            'q6-a': 'q6-compact', 'q6-b': 'q6-scheme', 'q6-complete': 'q6-scheme',
            **{k: 'q7-roof-section' for k in ['q7-a', 'q7-b-eaves', 'q7-b-ridge', 'q7-b', 'q7-complete']},
            'q8-a': 'q8-system', 'q8-b': 'q8-collector', 'q8-c-chimney': 'q8-locations', 'q8-c-hotpress': 'q8-locations', 'q8-c': 'q8-locations',
            'q8-complete': 'q8-scheme', **{k: 'q9-scheme' for k in ['q9-a', 'q9-b', 'q9-complete']},
            **{k: 'q10-scheme' for k in ['q10-a', 'q10-b', 'q10-c', 'q10-complete']}}
# A task named by reference to a printed list carries the scheme heading after ' — '.
LABELLED = {'q3-a-A', 'q3-a-B', 'q7-b-eaves', 'q7-b-ridge'}
SCHEME_PAGES = {'1': [4, 5, 6, 32], '2': [6, 7, 8, 33], '3': [9, 10, 34], '4': [11, 12, 13, 14, 35], '5': [15, 16, 17, 36],
                '6': [18, 19, 20, 37], '7': [21, 38], '8': [22, 23, 39], '9': [24, 25, 40], '10': [25, 26, 27, 28, 41],
                '10-alt': [29, 30, 42]}
PAPER_PAGE = {'1': 2, '2': 2, '3': 2, '4': 3, '5': 3, '6': 4, '7': 4, '8': 4, '9': 5, '10': 5, '10-alt': 5}


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


def printed(text):
    for glyph, letters in LIGATURES.items():
        text = text.replace(glyph, letters)
    return text


def region(qkey):
    text = printed(page_text(P, PAPER_PAGE[qkey]))
    if qkey == '10':
        return text[text.index(' 10. '):text.index(' OR ')]
    if qkey == '10-alt':
        return text[text.index(' OR ') + 4:]
    start = text.index(f' {qkey}. ')
    nxt = [text.index(f' {n}. ') for n in map(str, range(int(qkey) + 1, 11)) if f' {n}. ' in text]
    return text[start:min(nxt) if nxt else len(text)]


def qkey_of(key):
    return '10-alt' if key.startswith('q10-alt') else key[1:].split('-')[0]


def render(panels, gap=24):
    ims = []
    for source, page, rect in panels:
        with fitz.open(R / source) as pdf:
            px = pdf[page - 1].get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(rect), alpha=False)
        ims.append(Image.frombytes('RGB', (px.width, px.height), px.samples))
    if len(ims) == 1:
        return ims[0]
    out = Image.new('RGB', (max(i.width for i in ims), sum(i.height for i in ims) + gap * (len(ims) - 1)), 'white')
    y = 0
    for im in ims:
        out.paste(im, (0, y))
        y += im.height + gap
    return out


def validate(d, images=True, figure_dir=FIGURE_DIR, integrated=True):
    assert d['sourceHashes'] == HASHES
    for f, h in HASHES.items():
        assert hashlib.sha256((R / f).read_bytes()).hexdigest() == h, f
    assert (d['subjectId'], d['year'], d['level'], d['lang'], d['sitting'], d['paperKey'], d['fileid']) == (
        'construction-studies', 2015, 'higher', 'ev', 'main', 'single', 'LC029ALP000EV.pdf')
    cards = {t['card']['id'].removeprefix(PREFIX): t['card'] for t in d['tasks']}
    tasks = {t['card']['id'].removeprefix(PREFIX): t for t in d['tasks']}
    assert set(cards) == set(LEAF) | set(COMPOSITE) and len(d['tasks']) == len(cards) == 48
    assert d['addedIds'] == [t['card']['id'] for t in d['tasks'] if t['card']['id'].removeprefix(PREFIX) in ADDED]
    assert len(d['addedIds']) == 11 and all(t['correction'] == (k not in ADDED) for k, t in tasks.items())
    assert len({c['questionRef'] for c in cards.values()}) == 48
    bindings = {b['cardId'].removeprefix(PREFIX): b for b in d['bindings']}
    assert set(bindings) == set(cards) and len(d['bindings']) == 48
    scheme = normalise(' '.join(page_text(S, p) for p in range(1, 43)))
    crosswalk = json.loads((R / 'data/examTopics/construction-studies-curriculum-crosswalk.json').read_text())
    library_nodes = {n for nodes in crosswalk.values() for n in nodes}
    figures = {f['key'].removeprefix(FP): f for f in d['questionFigures']}
    assert set(figures) == set(SINGLE) | set(PANELS) and len(d['questionFigures']) == 25

    for key, c in cards.items():
        qk = qkey_of(key)
        q = '10' if qk == '10-alt' else qk
        t, b = tasks[key], bindings[key]
        assert t['questionNumber'] == b['questionNumber'] == q and t['alternative'] == (qk == '10-alt')
        assert (c['subjectId'], c['year'], c['level'], c['section']) == ('construction-studies', 2015, 'higher', 'B')
        assert c['tariffModel'] == {'kind': 'fixed'} and c['questionRef'].startswith(f'2015 HL Q{qk}')
        original = 'q10-alternative' if qk == '10-alt' else f'q{q}-original'
        assert c['questionFigureKey'] == FP + original and c['questionFigureIncludesPrompt'] is True
        assert c['sourceMaterial']['pages'] == [1, PAPER_PAGE[qk]] and t['requiredQuestionFigures'] == [c['questionFigureKey']]
        assert c.get('figureKey') == (FP + SOLUTION[key] if key in SOLUTION else None), key
        assert t['requiredSolutionFigures'] == ([FP + SOLUTION[key]] if key in SOLUTION else [])
        assert figures[original]['solution'] is False and (key not in SOLUTION or figures[SOLUTION[key]]['solution'] is True)
        # Lift, never write: printed wording only; a task named by reference carries the scheme heading.
        words = tokens(region(qk))
        heads, labels = [], []
        for para in c['questionText'].split('\n\n'):
            head, _, tail = para.partition(' — ')
            heads.append(head)
            labels += tail.split('; ') if tail else []
        assert is_subsequence(tokens(' '.join(heads)), words), (key, 'questionText not lifted')
        assert all(normalise(x) in scheme for x in labels), (key, 'label not printed in the scheme')
        assert bool(labels) == (key in LABELLED), (key, labels)
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
        assert 'questionBonus' not in c and c['totalMarks'] == sum(row['marks'] for row in c['rows'])
        assert c['totalMarks'] == PART_TOTALS[key], key
        if key in LEAF:
            assert [(row['id'], row['marks'], row.get('permittedMarks')) for row in c['rows']] == LEAF[key], key
            assert 'taskGroups' not in c
            nodes, topics = TOPICS[key]
            assert b['canonicalTopicIds'] == nodes and b['atlasTopicIds'] == [CROSS + x for x in topics], key
        else:
            kids = COMPOSITE[key]
            assert [g['sourceCardId'] for g in c['taskGroups']] == [PREFIX + k for k in kids] and len(kids) >= 2
            rows = []
            for kid, g in zip(kids, c['taskGroups']):
                rs = copy.deepcopy(cards[kid]['rows'])
                for row in rs:
                    row['id'] = kid.removeprefix(f'q{qk}-') + '-' + row['id']
                assert g['rowIds'] == [row['id'] for row in rs] and g['marks'] == cards[kid]['totalMarks'] and len(rs) <= 5 and g['label'].strip()
                rows += rs
            assert c['rows'] == rows, key
            assert b['canonicalTopicIds'] == list(dict.fromkeys(n for k in kids for n in bindings[k]['canonicalTopicIds']))
            assert b['atlasTopicIds'] == list(dict.fromkeys(x for k in kids for x in bindings[k]['atlasTopicIds']))
        assert b['markBankTopicId'] == c['topicId'] == b['canonicalTopicIds'][0]
        assert set(b['canonicalTopicIds']) <= library_nodes and len(set(b['canonicalTopicIds'])) == len(b['canonicalTopicIds'])
        assert all(x.startswith(CROSS) and x in crosswalk for x in b['atlasTopicIds']) and b['atlasTopicIds']
        assert len(b['canonicalTopicIds']) == 1 or b['canonicalTopicReview'].strip()
        assert [(x['file'], x['page']) for x in t['sourceChecks']] == [(P, 1), (P, PAPER_PAGE[qk])] + [(S, p) for p in [2, *SCHEME_PAGES[qk]]], key
        for x in t['sourceChecks']:
            assert hashlib.sha256(page_text(x['file'], x['page']).encode()).hexdigest() == x['textSha256'], (key, x)

    # Worked answers quoted in the calculation cards are the scheme's own figures.
    for key, page, values in [('q5-a', 15, ['0.02222222', '0.06944444', '8.06451613', '0.05454545', '8.45017269', '0.11834078']),
                              ('q5-b-new', 15, ['248.51563', '44.60']), ('q5-b-existing', 16, ['441', '79.14'])]:
        notes = ' '.join(row['contextNote'] for row in cards[key]['rows'])
        text = page_text(S, page)
        assert all(x in notes and x in text for x in values), (key, [x for x in values if x not in notes or x not in text])
    # The alternative Question 10 never combines with the Passive House question.
    for key, c in cards.items():
        for g in c.get('taskGroups', []):
            assert key.startswith('q10-alt') == g['sourceCardId'].startswith(PREFIX + 'q10-alt')
    # Choice is not a route: each printed choice is ONE card holding one anyN group over every printed item.
    for key, (rid, n, each, options) in CHOICES.items():
        assert [row['id'] for row in cards[key]['rows']] == [rid], key
        assert cards[key]['rows'][0]['group'] == dict(claimMax=n, perOption=each, options=options), key
    assert [k for k in cards if any(row['kind'] == 'anyN' for row in cards[k]['rows']) and k not in COMPOSITE] == list(CHOICES)
    assert not [k for k in cards if re.match(r'q(3-b|4-a|4-b|6-b|9-a|10-a)-.', k)], 'per-item, per-option or per-combination route cards'
    # One complete card per question, each worth 60.
    ledgers = d['questionRouteLedgers']
    for qk in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '10-alt']:
        whole = sorted(k for k in cards if k.startswith(f'q{qk}-complete') and qkey_of(k) == qk)
        assert len(whole) == 1 and [w['id'] for w in ledgers[qk]['wholeRoutes']] == [PREFIX + k for k in whole]
        assert all(cards[k]['totalMarks'] == 60 for k in whole)
    sel = d['selectionLedger']
    assert {k: v['cardId'] for k, v in sel['finiteQuestionChoices'].items()} == {
        '4a': PREFIX + 'q4-a', '4b': PREFIX + 'q4-b', '6b': PREFIX + 'q6-b', '9a': PREFIX + 'q9-a', '10a': PREFIX + 'q10-a'}
    assert {k: v['options'] for k, v in sel['finiteQuestionChoices'].items()} == {
        k.replace('q', '').replace('-', ''): v[3] for k, v in CHOICES.items()}
    assert sel['optionSelectionsMarkedAlike'] == {'3b': dict(options=['(i) extension at A', '(ii) detached space at B'], cardId=PREFIX + 'q3-b')}
    assert sel['unclassified'] == 0 and all(x['classification'] for x in sel['rows'])
    observed = []
    with fitz.open(R / P) as pdf:
        for i, p in enumerate(pdf):
            observed.extend((i + 1, m.start(), m.group()) for m in re.finditer(sel['pattern'], ' '.join(p.get_text().split()), re.I))
    assert observed == [(x['page'], x['start'], x['match']) for x in sel['rows']] and len(observed) == 15

    for key, f in figures.items():
        if key in SINGLE:
            assert (f['source'], f['page'], f['rect'], f['solution']) == SINGLE[key] and 'panels' not in f, key
            panels = [SINGLE[key][:3]]
        else:
            spec, solution = PANELS[key]
            assert f['panels'] == [dict(source=s, page=p, rect=rc) for s, p, rc in spec] and f['solution'] == solution and f['panelGap'] == 24, key
            panels = spec
        assert f['visuallyInspected'] and f['renderScale'] == 2
        path = Path(figure_dir) / f"{f['key']}.png"
        assert hashlib.sha256(path.read_bytes()).hexdigest() == f['sha256'], key
        if images:
            a, saved = render(panels), Image.open(path).convert('RGB')
            assert a.size == saved.size and ImageChops.difference(a, saved).getbbox() is None, key
    assert len({f['sha256'] for f in d['questionFigures']}) == 25

    # In-place corrections: same ID, concept ID and tariff, hash-linked to the earlier card they replace.
    legacy = {c['id']: c for c in json.loads((DRAFTS / 'prior-2015-higher-cards.json').read_text())}
    assert len(legacy) == 102 and set(cards) - ADDED == {k.removeprefix(PREFIX) for k in legacy} & set(cards)
    fixes = {x['cardId']: x for x in d['corrections']}
    assert set(fixes) == {PREFIX + k for k in cards if k not in ADDED} and len(d['corrections']) == 37
    for cid, fix in fixes.items():
        old, new = legacy[cid], cards[cid.removeprefix(PREFIX)]
        assert fix['priorSha256'] == construction_corrections.card_hash(old) and fix['correctedSha256'] == construction_corrections.card_hash(new), cid
        assert new['conceptId'] == old['conceptId'] and new['totalMarks'] == old['totalMarks'] and fix['reason'].strip(), cid
        assert (fix['priorTotalMarks'], fix['correctedTotalMarks'], fix['priorTopicId'], fix['correctedTopicId']) == (
            old['totalMarks'], new['totalMarks'], old['topicId'], new['topicId']), cid
    retired = set(legacy) - {PREFIX + k for k in cards}
    assert len(retired) == 65

    authored = json.loads((R / 'scripts/markbank/authored/construction-studies.json').read_text())
    by_id = {c['id']: c for c in authored}
    assert len(by_id) == len(authored)
    if integrated:
        prior = json.loads((DRAFTS / 'prior-authored-card-hashes.json').read_text())
        assert prior['count'] == len(prior['cards']) == 764
        for cid, fix in fixes.items():
            assert prior['cards'][cid] == fix['priorSha256'], cid
        construction_corrections.assert_prior_cards_preserved(prior['cards'], by_id)
        assert all(by_id[t['card']['id']] == t['card'] for t in d['tasks'])
        assert sorted(c for c in by_id if c.startswith(PREFIX)) == sorted(t['card']['id'] for t in d['tasks'])
        # Every earlier route task is withdrawn through a recorded, hash-linked withdrawal (branch-only: no alias).
        gone = {w['cardId']: w for w in d['withdrawn']}
        assert set(gone) == retired and all(gone[c]['priorSha256'] == prior['cards'][c] and 'aliasOf' not in gone[c] for c in retired)
        for name in ['card-source-bindings.json', 'card-corrections.json']:
            overrides = json.loads((R / 'scripts/markbank' / name).read_text()).get('construction-studies', {})
            assert not [k for k in overrides if k.startswith(PREFIX)], name
    elif integrated is False:
        assert all(construction_corrections.card_hash(by_id[cid]) == fixes[cid]['priorSha256'] for cid in fixes)
    assert d['questionsReviewed'] == [str(n) for n in range(1, 11)] and d['unreviewedQuestions'] == [] and d['alternativeQuestions'] == ['10']
    return dict(tasks=48, addedTasks=11, correctedTasks=37, withdrawnTasks=65, leafTasks=len(LEAF),
                wholeQuestions=sum(1 for k in cards if '-complete' in k), anyNChoiceCards=len(CHOICES), sourceFigures=25, paperComplete=True)


if __name__ == '__main__':
    print(json.dumps(validate(json.loads(REVIEW.read_text()))))
