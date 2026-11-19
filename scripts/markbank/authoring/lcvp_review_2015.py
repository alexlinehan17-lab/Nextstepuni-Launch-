#!/usr/bin/env python3
"""Hash-bound selectors following the independent 54-page 2015 visual sweep."""
import hashlib
import json
import re
import sys
import fitz
from lcvp_review_2026 import ROOT, tidy, select, point, criterion
from lcvp_review_2024 import split_raw
from lcvp_review_2022 import page_raw
from lcvp_review_2018 import choice_row, response_row, before_rate, models
from lcvp_review_2017 import paper_raw, header_body, component_rows
from lcvp_identity import concept_id

REVIEW = ROOT / 'scripts/markbank/authoring/lcvp/2015-cl-main-review.json'
PAPER = 'paper-trail-corpus/exampapers/2015/LC462CLP000EV.pdf'
CASE = 'paper-trail-corpus/exampapers/2015/LC462CLP016EV.pdf'
SCHEME = 'paper-trail-corpus/markingschemes/2015/LC462CLP000EV.pdf'
HASHES = {PAPER: '535d587fe354959c1a99a6155032a2931f6307095c09ed9701df0cff3d2f26e6',
          CASE: '0d82ba4196faade2812abe2925179454079c6f790e97d96f333c4bf8c28997ec',
          SCHEME: '6905321d42cfa0d8da3e9b167a1441fb5bb328eb033a169addcb5cdbbe3288a1'}
VIDEO_URL = 'https://www.examinations.ie/archive/exampapers/2015/LC462CLPO31EV.mp4'


def documents():
    for path, expected in HASHES.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
    return fitz.open(ROOT / PAPER), fitz.open(ROOT / SCHEME)


def key(section, q, letter=None, roman=None):
    return section, q, letter, roman


def scheme_parts(doc):
    sections = split_raw('\n'.join(page_raw(doc, n) for n in range(4, 17)),
                         r'^\s*Section ([ABC])\s+', list('ABC'))
    out = {}
    for section, value in sections.items():
        questions = split_raw(value, r'^\s*Q\.?\s*(\d+)\s*',
            [str(n) for n in range(1, {'A': 8, 'B': 3, 'C': 6}[section] + 1)])
        for q, block in questions.items():
            q = int(q)
            if section == 'A' or (section == 'B' and q == 1):
                out[key(section, q)] = block
            elif section == 'B':
                heading, body = header_body(block)
                for roman, part in split_raw(body, r'^\s*\((i{1,3})\)\s*', ['i', 'ii', 'iii'] if q == 2 else ['i', 'ii']).items():
                    out[key(section, q, None, roman)] = heading + '\n' + part
            else:
                for letter, part in split_raw(block, r'^\s*\(([abcd])\)\s*', list('abcd')).items():
                    if (q, letter) in [(2, 'a'), (4, 'a'), (4, 'c'), (5, 'b'), (6, 'b')]:
                        heading, body = header_body(part)
                        for roman, answer in split_raw(body, r'^\s*\((i{1,2})\)\s*', ['i', 'ii']).items():
                            out[key(section, q, letter, roman)] = heading + '\n' + answer
                    else:
                        out[key(section, q, letter)] = part
    assert len(out) == 43
    return out


PAGES = {key('A', q): [p] for q, p in enumerate([3, 3, 3, 4, 4, 5, 6, 7], 1)}
PAGES[key('A', 5)] = [4, 5]
PAGES[key('B', 1)] = [9]
PAGES.update({key('B', q, None, roman): [8 + q, 9 + q]
              for q in [2, 3] for roman in (['i', 'ii', 'iii'] if q == 2 else ['i', 'ii'])})
PAGES.update({key('C', q, letter): [14 + (q - 1) * 3 + {'a': 0, 'b': 0, 'c': 1, 'd': 2}[letter]]
              for q in range(1, 7) for letter in 'abcd'})
PAGES[key('C', 1, 'd')] = [15, 16]
PAGES[key('C', 5, 'd')] = [27, 28]
for k in [key('C', 3, 'b'), key('C', 3, 'c'), key('C', 4, 'b'), key('C', 4, 'c')]:
    PAGES[k].append(PAGES[k][0] + 1)
for q, letter in [(2, 'a'), (4, 'a'), (4, 'c'), (5, 'b'), (6, 'b')]:
    pages = PAGES.pop(key('C', q, letter))
    PAGES.update({key('C', q, letter, roman): pages for roman in ['i', 'ii']})


def question(doc, k):
    section, q, letter, roman = k
    value = paper_raw(doc, PAGES[k][0])
    if section in ['A', 'B']:
        value = re.split(r'^\s*Q\.\s*' + str(q) + r'\s+', value, maxsplit=1, flags=re.M)[1]
        value = re.split(r'^\s*Q\.\s*\d+\s+', value, maxsplit=1, flags=re.M)[0]
    if letter:
        value = re.split(r'\(' + letter + r'\)\s*', value, maxsplit=1)[1]
        value = re.split(r'\([abcd]\)\s*', value, maxsplit=1)[0]
    if roman:
        value = re.split(r'\(' + roman + r'\)\s*', value, maxsplit=1)[1]
        value = re.split(r'\(i{1,3}\)\s*', value, maxsplit=1)[0]
    value = tidy(re.sub(r'\b\d+\s+marks?\b', '', value, flags=re.I))
    if k == key('B', 1):
        # Five visually reviewed round bullets: the original SymbolMT font
        # encodes these particular marks as U+F0B7. This is not a global map.
        bullets = [s for b in doc[8].get_text('dict')['blocks']
                   for line in b.get('lines', []) for s in line['spans'] if '\uf0b7' in s['text']]
        assert len(bullets) == value.count('\uf0b7') == 5
        assert all(s['font'] == 'SymbolMT' and s['text'] == '\uf0b7' for s in bullets)
        value = value.replace('\uf0b7', '•')
    if k == key('C', 2, 'b'):
        # Physical17 has an isolated dot in unused answer space and a tiny
        # 4 below the answer box. Full-page visual review and exact geometry
        # bind this exception; neither artifact belongs to the printed stem.
        prompt = 'Explain how a local voluntary body differs from a commercial business.'
        assert value == prompt + ' . 4', value
        spans = [s for b in doc[16].get_text('dict')['blocks']
                 for line in b.get('lines', []) for s in line['spans']]
        assert len([s for s in spans if s['text'].strip() == '.' and 432 < s['bbox'][1] < 433]) == 1
        assert len([s for s in spans if s['text'].strip() == '4' and 800 < s['bbox'][1] < 801 and s['size'] < 4.1]) == 1
        value = prompt
    return value


def contrast_models(scheme):
    """Select both original ruled cells in each of the six contrast rows."""
    page = scheme[8]
    dividers = [item[1] for drawing in page.get_drawings() for item in drawing['items']
                if item[0] == 're' and item[1].width < 1 and item[1].height > 10
                and 200 < item[1].x0 < 400]
    assert dividers, 'Original central table divider missing'
    split_x = min((r.x0 for r in dividers), key=lambda x: abs(x - page.rect.width / 2))
    bounds = sorted({(r.y0, r.y1) for r in dividers if abs(r.x0 - split_x) < .1})
    assert len(bounds) == 7, bounds  # one heading row, six original model rows
    result = []
    for number, (upper, lower) in enumerate(bounds[1:], 1):
        cells = []
        for left in [True, False]:
            pieces = []
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines', []):
                    # Text is vertically centred independently in each cell;
                    # left-hand line starts would truncate right-hand row5.
                    # Font boxes overlap rules, so bind by span centres.
                    spans = [s for s in line['spans'] if upper <= (s['bbox'][1] + s['bbox'][3]) / 2 <= lower
                             and bool((s['bbox'][0] + s['bbox'][2]) / 2 < split_x) == left]
                    if spans:
                        pieces.append((line['bbox'][1], line['bbox'][0], ''.join(s['text'] for s in spans)))
            cell = tidy(' '.join(value for _, _, value in sorted(pieces)))
            assert cell.startswith(str(number) + '.'), (number, left, cell)
            cell = re.sub(r'^' + str(number) + r'\.\s*', '', cell)
            assert cell, (number, left)
            cells.append(cell)
        result.append(cells[0] + ' — ' + cells[1])
    return result


def source(pages, kind='source-question', title='Original question'):
    return dict(kind=kind, label='OFFICIAL SOURCE', title=title, pages=pages,
        attribution='SEC LCVP Link Modules 2015 Common Level — © State Examinations Commission.',
        presentationNote='Read the complete original source and question in context.')


def build():
    paper, scheme = documents()
    raw = scheme_parts(scheme)
    rows, totals, topics, concepts = {}, {}, {}, {}
    a = lambda q: key('A', q)
    b = lambda q, r=None: key('B', q, None, r)
    c = lambda q, l, r=None: key('C', q, l, r)
    held = {b(2, 'ii')}
    def put(k, marks, topic, concept, value):
        rows[k], totals[k], topics[k], concepts[k] = value, marks, topic, concept
    def labelled(k):
        header, body = header_body(raw[k])
        if k[3]:
            header = split_raw(header, r'^\s*\((i{1,3})\)\s*',
                ['i', 'ii', 'iii'] if k[0] == 'B' and k[1] == 2 else ['i', 'ii'])[k[3]]
        return tidy(re.sub(r'\b\d+\s+[Mm]arks?\b', '', header)), body
    def ordinary(k, topic, concept, count, per, expected, rate, binary=False, extra=''):
        label, body = labelled(k)
        pool = models(before_rate(body, rate), expected)
        if binary or per == 1:
            value = choice_row('responses', label, pool, count, per,
                f'Original {count} responses at {per} or 0 marks each. All alternatives remain. ' + extra)
        else:
            value = response_row('responses', label, pool, count, list(range(per + 1)),
                f'Original {count} responses, each {per} marks in printed 1-mark components. ' + extra)
        put(k, count * per, topic, concept, [value])
    def definition(k, topic, concept, count, steps, rate, note=''):
        label, body = labelled(k)
        put(k, count * steps[-1], topic, concept, [response_row('definition', label,
            [tidy(before_rate(body, rate))], count, steps,
            'Preserve the full original definition. No fixed semantic division is inferred. ' + note)])
    def named_components(k, topic, concept, count, expected, rate, labels, extra=''):
        label, body = labelled(k)
        pool = models(before_rate(body, rate), expected)
        value = component_rows(label, pool, [[1] * len(labels)] * count,
            'Original explicit components: ' + ', '.join(title + ' 1m' for title in labels) + '. ' + extra)
        for row in value:
            for part, title in zip(row['parts'], labels):
                part['verbatim'] = title
        put(k, count * len(labels), topic, concept, value)

    _, body = labelled(a(1))
    put(a(1), 1, '1-1', 'recording-studio-business', [point('business', tidy(before_rate(body, r'1m')), 1)])
    label, body = labelled(a(2))
    put(a(2), 2, '1-1', 'business-suitability', component_rows(label,
        models(before_rate(body, r'2m'), 3), [[1, 1]],
        'Original total 2m (1+1). Keep the why-question and all three model reasons; no prescribed count of reasons or fixed semantic split is added.'))
    label, body = labelled(a(3))
    parts = split_raw(body, r'^\s*\((i{1,2})\)\s*', ['i', 'ii'])
    put(a(3), 3, '1-1', 'wedding-band-niche-market', [point('market', tidy(before_rate(parts['i'], r'1m')), 1),
        choice_row('reason', label, models(before_rate(parts['ii'], r'2m'), 4), 1, 2,
            'One complete compound task: niche market 1m plus reason 2m (0/2). All four reason models remain; no 1-mark partial for the reason.')])
    ordinary(a(4), '1-1', 'previous-business-learning', 2, 2, 2, r'2\s*@\s*2m', binary=True)
    ordinary(a(5), '1-1', 'local-enterprise-office-support', 2, 2, 3, r'2\s*@\s*2m', binary=True)
    ordinary(a(6), '1-1', 'business-idea-problems', 2, 2, 4, r'2\s*@\s*2m', binary=True)
    _, body = labelled(a(7))
    parts = split_raw(body, r'^\s*\((i{1,2})\)\s*', ['i', 'ii'])
    put(a(7), 6, '1-1', 'business-plan-importance-improvements', [
        choice_row('importance', 'Explain the importance of a business plan.', models(before_rate(parts['i'], r'1\s*@\s*2m'), 4), 1, 2,
            'Original importance 1@2m (0/2); retain all four models.'),
        choice_row('improvements', 'Suggest how Sylvia could improve her business plan for the next meeting with Seán.', models(before_rate(parts['ii'], r'2\s*@\s*2m'), 5), 2, 2,
            'Original improvements 2@2m (0/2); retain all five models. The complete two-part paper question remains one 6-mark task.')])
    ordinary(a(8), '1-1', 'enterprise-mentoring-benefits', 3, 2, 4, r'3\s*@\s*2\s*m',
        extra='The fourth original model includes all six printed business-support areas; they are not discarded or substituted for the full pool.')

    ordinary(b(1), '1-1', 'business-case-definitions', 3, 2, 5, r'3\s*@\s*2\s*m',
        extra='Explain THREE of the FIVE printed terms. All five full definitions remain visible in one task.')
    definition(b(2, 'i'), '1-1', 'corporate-social-responsibility-definition', 2, [0, 2], r'2\s*@\s*2m',
        'Original 2@2m (0/2); no 1-mark intermediate or fixed descriptor pairing.')
    _, body = labelled(b(2, 'ii'))
    alternatives = re.split(r'^\s*or\s*$', body, maxsplit=1, flags=re.M)
    assert len(alternatives) == 2 and '2m' in alternatives[0] and re.search(r'2\s*@\s*1m', alternatives[0])
    assert 'fully serviced desks' in alternatives[1] and 'legal and tax issues' in alternatives[1]
    alternatives = [re.sub(r'^\s*[12]\.\s*', '', value) for value in alternatives]
    guidance = ('Numeric scoring held. One complete 4-mark policy task. The first route prints 2m (0/2) for the Careers Programme plus 2@1m for details. '
        'The complete OR alternative for start-up enterprises has no printed internal allocation. The parent 12 marks, with 4 for (i) and 4 for (iii), binds this whole total. '
        'Keep both alternatives and the literal first-route tariffs; confidence review only pending authoritative clarification. Do not transfer the split to the second alternative or offer only the priced route.')
    put(b(2, 'ii'), 4, '1-1', 'csr-policy-alternatives', [point('careers-policy', tidy(alternatives[0]), note=guidance),
        point('startup-policy', tidy(alternatives[1]), note='or — Complete second policy alternative. No internal tariff is printed for this route; retain its full text in this whole-task confidence review.')])
    ordinary(b(2, 'iii'), '1-1', 'csr-strategy-areas', 2, 2, 4, r'2\s*@\s*2m', binary=True)
    definition(b(3, 'i'), '1-1', 'case-diversification-definition', 2, [0, 2], r'2\s*@\s*2\s*m',
        'Original 2@2m (0/2). Keep the full definition and all three case examples; no unprinted fixed definition/example weighting.')
    ordinary(b(3, 'ii'), '1-1', 'diversification-reasons', 4, 2, 6, r'4\s*@\s*2m')

    _, body = labelled(c(1, 'a'))
    assert re.fullmatch(r'Name\s+2m\s+Outline of activity\s+2m\s+\(1\s*\+\s*1\)', body.strip())
    put(c(1, 'a'), 4, '1-3', 'planned-lcvp-activity', [point('name', 'Name', 2,
        'Name 2m has no internal 1-mark split.'), criterion('outline', 'Outline of activity', 1, [0, 1, 2],
        'Original Outline of activity 2m (1+1). Use the same named activity; no personal example is invented.')])
    ordinary(c(1, 'b'), '1-3', 'activity-planning-benefits', 3, 2, 6, r'3\s*@\s*2m')
    ordinary(c(1, 'c'), '1-3', 'activity-research-methods', 3, 2, 6, r'3\s*@\s*2m',
        extra='The method of research must be specific to the activity named in part (a).')
    named_components(c(1, 'd'), '1-3', 'activity-evaluation-methods', 3, 6, r'3\s*@\s*3m', ['Method', 'Explanation', 'Why'],
        'All six original methods and every nested bullet remain, including the continuation onto scheme physical9.')
    _, body = labelled(c(2, 'a', 'i'))
    put(c(2, 'a', 'i'), 1, '1-2', 'named-voluntary-body', [point('name', tidy(before_rate(body, r'1m')), 1)])
    definition(c(2, 'a', 'ii'), '1-2', 'volunteer-definition', 2, [0, 1], r'2m', 'Original 2m (1+1).')
    label, _ = labelled(c(2, 'b'))
    put(c(2, 'b'), 6, '1-2', 'voluntary-commercial-comparison', [response_row('comparisons', label,
        contrast_models(scheme), 3, [0, 1, 2],
        'Original 3@2m (1+1). Each paired model reads Voluntary Bodies — Commercial Business. Keep both complete table cells for each comparison, all six pairs and every wrapped line.')])
    ordinary(c(2, 'c'), '1-2', 'voluntary-body-community-benefits', 4, 2, 6, r'4\s*@\s*2m')
    ordinary(c(2, 'd'), '1-2', 'volunteer-ethical-obligations', 4, 2, 8, r'4\s*@\s*2m')
    ordinary(c(3, 'a'), '0-3', 'finding-work-placement', 3, 1, 7, r'3\s*@\s*1m')
    _, body = labelled(c(3, 'b'))
    entries = re.findall(r'^\s*(\S[^\n]*?)\s+([12])m\s*$', body, re.M)
    assert len(entries) == 7 and [int(m) for _, m in entries] == [1, 1, 1, 2, 1, 2, 2], entries
    assert '* compulsory item' in body and entries[5][0] == 'Closing paragraph (*CV enc)'
    put(c(3, 'b'), 10, '0-3', 'work-placement-request-letter', [dict(id='letter', kind='criterion',
        verbatim=question(paper, c(3, 'b')), marks=10, permittedMarks=list(range(11)),
        parts=[dict(id=f'criterion-{i}', verbatim=tidy(label), marks=int(mark), permittedMarks=[0, int(mark)])
               for i, (label, mark) in enumerate(entries, 1)],
        contextNote='One complete letter requesting a THREE DAY placement. Retain all seven source criteria and their 1/1/1/2/1/2/2 allocations. * compulsory item: CV enclosure in the closing paragraph. The source supplies no internal 1-mark intermediate for its 2-mark criteria; do not invent one. Addresses together receive one mark.')])
    ordinary(c(3, 'c'), '0-0', 'employability-characteristics', 3, 2, 6, r'3\s*@\s*2m', extra='This list is not exhaustive.')
    ordinary(c(3, 'd'), '0-3', 'placement-working-world-preparation', 3, 2, 5, r'3\s*@\s*2m')
    definition(c(4, 'a', 'i'), '0-0', 'trade-union-definition', 3, [0, 1], r'3\s*@\s*1m', 'Original 3@1m.')
    _, body = labelled(c(4, 'a', 'ii'))
    names = select(tidy(before_rate(body, r'2\s*@\s*1m')), 'Name any two trade unions').split('/')
    assert len(names) == 9
    put(c(4, 'a', 'ii'), 2, '0-0', 'trade-union-examples', [choice_row('names', question(paper, c(4, 'a', 'ii')), names, 2, 1,
        'Name ANY TWO trade unions, 2@1m. Preserve all nine original alternatives; the list is open.')])
    ordinary(c(4, 'b'), '0-0', 'trade-union-member-benefits', 4, 2, 7, r'4\s*@\s*2m')
    definition(c(4, 'c', 'i'), '0-0', 'employment-contract-definition', 2, [0, 1], r'2m',
        'Original 2m (1+1). The source stars “written document” and states “* compulsory item”; this required wording remains visible with the full definition.')
    ordinary(c(4, 'c', 'ii'), '0-0', 'employment-contract-content', 4, 1, 9, r'4\s*@\s*1m')
    ordinary(c(4, 'd'), '0-0', 'employer-safety-responsibilities', 3, 2, 6, r'3\s*@\s*2m')
    definition(c(5, 'a'), '0-2', 'career-investigation-definition', 2, [0, 1], r'2m', 'Original 2m (1+1).')
    _, body = labelled(c(5, 'b', 'i'))
    put(c(5, 'b', 'i'), 1, '0-2', 'investigated-career-name', [point('career', tidy(before_rate(body, r'1m')), 1)])
    ordinary(c(5, 'b', 'ii'), '0-2', 'career-investigation-steps', 4, 1, 7, r'4\s*@\s*1m')
    _, body = labelled(c(5, 'c'))
    assert re.search(r'State the two subjects\s+2\s*@\s*1m', body)
    assert re.search(r'Explain the relevance of the subjects\s+2\s*@\s*2m', body)
    profiles = []
    for i in range(1, 3):
        profiles.append(dict(id=f'subject-{i}', kind='criterion', verbatim=labelled(c(5, 'c'))[0],
            marks=3, permittedMarks=list(range(4)),
            parts=[dict(id='subject', verbatim='Subject', marks=1, permittedMarks=[0, 1]),
                   dict(id='relevance', verbatim='Relevance', marks=2, permittedMarks=[0, 1, 2])],
            contextNote=f'Subject/relevance profile {i} of 2 for the SAME named career. Source: State the two subjects 2@1m; Explain the relevance of the subjects 2@2m (1+1). Keep both complete profiles; no specific subjects are invented.'))
    put(c(5, 'c'), 6, '0-2', 'career-subjects-relevance', profiles)
    _, body = labelled(c(5, 'd'))
    heading_text = before_rate(body, r'\[6\s*@\s*1m\]\s*x\s*2')
    headings = [tidy(line) for line in heading_text.splitlines() if line.strip()]
    assert len(headings) == 6 and headings[0] == 'Course Title' and headings[-1] == 'End qualification/name of qualification'
    pathways = []
    for i in range(1, 3):
        pathways.append(dict(id=f'pathway-{i}', kind='criterion', verbatim=question(paper, c(5, 'd')), marks=6, permittedMarks=list(range(7)),
            parts=[dict(id=f'heading-{j}', verbatim=h, marks=1, permittedMarks=[0, 1]) for j, h in enumerate(headings, 1)],
            contextNote=f'Pathway {i} of TWO complete pathways to the same chosen career. Original [6@1m]x2; every one of the six named headings receives one mark in each pathway. No choose-some rule or invented course is introduced.'))
    put(c(5, 'd'), 12, '0-2', 'two-career-pathways', pathways)
    ordinary(c(6, 'a'), '1-3', 'loom-band-idea-generation', 4, 1, 8, r'4\s*@\s*1m')
    definition(c(6, 'b', 'i'), '1-3', 'market-research-definition', 2, [0, 1], r'2\s*@\s*1m', 'Original 2@1m.')
    _, body = labelled(c(6, 'b', 'ii'))
    pool = select(tidy(before_rate(body, r'3\s*@\s*1m')), 'Methods of market research').split('/')
    assert len(pool) == 8
    put(c(6, 'b', 'ii'), 3, '1-3', 'other-market-research-tools', [choice_row('methods', question(paper, c(6, 'b', 'ii')), pool, 3, 1,
        'Original 3@1m. The paper excludes questionnaires; retain all eight slash-separated source methods.')])
    named_components(c(6, 'c'), '1-3', 'questionnaire-disadvantages', 4, 9, r'4\s*@\s*2m', ['Statement', 'Disadvantage'])
    named_components(c(6, 'd'), '1-3', 'loom-band-ict-uses', 4, 9, r'4\s*@\s*2m', ['Method', 'Use'])
    assert set(rows) == set(raw) == set(PAGES) and len(rows) == 43
    assert sum(totals.values()) == 210 and sum(totals[k] for k in held) == 4

    case = select(tidy(paper_raw(paper, 8)), 'Section B Case Study 30 marks')
    stems = {q: tidy(re.split(r'^Q\.\s*' + str(q) + r'\s+', paper_raw(paper, 14 + (q - 1) * 3), maxsplit=1, flags=re.M)[1].split('(a)', 1)[0]) for q in range(1, 7)}
    cards = []
    for k in raw:
        section, q, letter, roman = k
        suffix = section.lower() + str(q) + (letter or '') + (roman or '')
        card_id = 'lcvp-2015-cl-' + suffix
        ref = f'2015 CL Section {section} Q{q}' + (f'({letter})' if letter else '') + (f'({roman})' if roman else '')
        card = dict(id=card_id, subjectId='lcvp', topicId='lcvp-link-modules-' + topics[k],
            conceptId=concept_id(card_id, concepts[k]), level='common', year=2015, section=section,
            questionRef=ref, questionText=question(paper, k), stem=case if section == 'B' else stems[q] if section == 'C' else '',
            figureKey='', labelKey=[], totalMarks=totals[k], rows=rows[k],
            tariffModel=dict(kind='questionTotal' if k in held else 'fixed', notation='Original 2015 marking scheme allocation.'),
            sourceMaterial=source(PAGES[k]))
        if section == 'C' and q == 1 and letter in 'bcd':
            card['stem'] += ' ' + question(paper, c(1, 'a'))
        if section == 'C' and q == 2 and letter in 'bcd':
            card['stem'] += ' ' + question(paper, c(2, 'a', 'i'))
        if section == 'C' and q == 5 and (k == c(5, 'b', 'ii') or letter in 'cd'):
            card['stem'] += ' ' + question(paper, c(5, 'b', 'i'))
        if section == 'C' and q == 6 and letter == 'b':
            card['stem'] += ' ' + select(tidy(paper_raw(paper, 29)), '(b)', '(i)')
        if section == 'A':
            card['videoMaterial'] = dict(kind='source-video', label='OFFICIAL VIDEO', title='2015 LCVP audiovisual examination',
                playbackUrl=VIDEO_URL, canonicalUrl=VIDEO_URL, secFileid='LC462CLPO31EV.mp4',
                attribution='State Examinations Commission — original 2015 Common Level English audiovisual recording.',
                presentationNote='Watch the original enterprise sequence with its sound before answering. Follow the printed viewing instructions. Use the original source link if embedded playback is unavailable.')
            card['additionalSourceMaterials'] = [source([2], title='Original audiovisual instructions')]
        elif section == 'B':
            card['sourceMaterial'] = source([8], 'source-text', 'Recruit Me Ltd — complete case study')
            card['sourceMaterial']['presentationNote'] += ' Preserve the original Social Entrepreneurs Ireland logo and full five-paragraph context.'
            card['additionalSourceMaterials'] = [source(PAGES[k])]
        for row in card['rows']:
            if row.get('contextNote') == '':
                row.pop('contextNote')
        cards.append(card)
    return cards, scheme


def scheme_page_text(scheme, number):
    return scheme[number - 1].get_text(sort=number != 9)


def write(cards, scheme):
    review = json.loads(REVIEW.read_text())
    proof = review['sourceVerification']['proof']
    digest = hashlib.sha256(json.dumps(cards, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    assert proof['tasks'] == review['manualPricedTasks'] == 43
    assert digest == proof['authoredSubsetSha256'], 'Refresh the mandatory original-source gate before writes'
    assert review['sourceVerification']['validatedAuthoringSha256'] == hashlib.sha256((ROOT / 'scripts/markbank/authoring/lcvp_review_2015.py').read_bytes()).hexdigest()
    path = ROOT / 'scripts/markbank/authored/lcvp.json'
    old = json.loads(path.read_text())
    preserved = [c for c in old if c['year'] != 2015]
    prior = [c for c in old if c['year'] == 2015]
    assert len(prior) in [0, 43] and len(preserved) == 475
    assert {c['id']: c['conceptId'] for c in prior}.items() <= {c['id']: c['conceptId'] for c in cards}.items()
    result, inserted = [], False
    for card in old:
        if card['year'] == 2015:
            if not inserted:
                result.extend(cards)
                inserted = True
        else:
            result.append(card)
    if not inserted:
        result.extend(cards)
    assert [c for c in result if c['year'] != 2015] == preserved
    path.write_text(json.dumps(result, ensure_ascii=False, indent=1) + '\n')
    pages = [f'## Physical page {n}\n\n' + scheme_page_text(scheme, n) for n in range(1, 21)]
    transcript = '# SEC LCVP 2015 Common Level written marking scheme\n\n' + '\n\n'.join(pages)
    (ROOT / 'examiner-reports/lcvp/schemes/2015-cl.md').write_text('\n'.join(line.rstrip() for line in transcript.splitlines()).rstrip() + '\n')
    review['status'] = 'source-authored; independent-sweep-complete; validation-pending'
    review['tasks'] = [dict(id=c['id'], questionRef=c['questionRef'], marks=c['totalMarks'], topicId=c['topicId']) for c in cards]
    REVIEW.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    cards, scheme = build()
    if '--write' in sys.argv:
        write(cards, scheme)
    else:
        print(json.dumps(cards, ensure_ascii=False, indent=2))
