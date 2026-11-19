#!/usr/bin/env python3
"""Source-lifted 2025 LCVP after the independent 62-page visual census.

Replace this sitting only, preserving its 42 existing IDs and adding the three
omitted tasks. The independent manual ledger precedes these PDF selectors.
"""
import hashlib
import json
import re
import sys
import fitz
from lcvp_identity import concept_id
from lcvp_review_2026 import (ROOT, tidy, select, page_text, numbered, split_heads,
                              point, criterion, menu, partial)

REVIEW = ROOT / 'scripts/markbank/authoring/lcvp/2025-cl-main-review.json'
PAPER = 'paper-trail-corpus/exampapers/2025/LC462CLP000EV.pdf'
SCHEME = 'paper-trail-corpus/markingschemes/2025/LC462CLP000EV.pdf'
HASHES = {PAPER: '070e0bc008f187ce2fdb833997be0d9a640ded62a5c92282bf33de6fefa6c0ce',
          SCHEME: 'c1d5ecb2fae99f3b47d8c21e0ae5af69291efeb1b925203f2418a117642f29af'}
VIDEO_URL = 'https://www.examinations.ie/archive/exampapers/2025/LC462CLP031EV.mov'


def documents():
    for path, expected in HASHES.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
    return fitz.open(ROOT / PAPER), fitz.open(ROOT / SCHEME)


def scheme_parts(doc):
    sections = split_heads(' '.join(page_text(doc, n) for n in range(4, 20)),
                           r'Section ([ABC])\s+', list('ABC'))
    out = {}
    for section, value in sections.items():
        questions = split_heads(value, r'Q\.\s*(\d+)\s+',
                                [str(n) for n in range(1, {'A': 8, 'B': 3, 'C': 7}[section] + 1)])
        for q, block in questions.items():
            if section == 'A':
                if q == '6':
                    # The asks and allocation each repeat (i)/(ii); start at the allocation.
                    allocation = select(block, '6 marks')
                    for roman, part in split_heads(allocation, r'\((i{1,2})\)\s+', ['i', 'ii']).items():
                        out[(section, 6, None, roman)] = part
                else:
                    out[(section, int(q), None, None)] = block
            elif section == 'B':
                if q == '1':
                    out[(section, 1, None, None)] = block
                else:
                    for roman, part in split_heads(block, r'(?<!part )\((i{1,3})\)\s+', ['i', 'ii', 'iii']).items():
                        out[(section, int(q), None, roman)] = part
            else:
                # The source's narrow left-margin (d) may be omitted by a PDF text clip.
                # Exact repeated question wording binds this boundary independently.
                if q == '6':
                    anchor = 'How may a business fund the cost of upgrading or improving ICT'
                    assert block.count(anchor) == 1
                    before, after = block.split(anchor)
                    before = re.sub(r'\(d\)\s*$', '', before)
                    block = before + ' (d) ' + anchor + after
                for letter, part in split_heads(block, r'(?<!part )\(([abcd])\)\s+', list('abcd')).items():
                    if q == '7' and letter == 'a':
                        for roman, sub in split_heads(part, r'\((i{1,2})\)\s+', ['i', 'ii']).items():
                            out[(section, 7, letter, roman)] = sub
                    else:
                        out[(section, int(q), letter, None)] = part
    assert len(out) == 45, len(out)
    return out


PAGES = {('A', q, None, None): p for q, p in enumerate([4, 4, 4, 5, 5, 6, 7, 8], 1)}
PAGES.pop(('A', 6, None, None))
PAGES.update({('A', 6, None, r): 6 for r in ['i', 'ii']})
PAGES[('B', 1, None, None)] = 10
PAGES.update({('B', q, None, r): 9 + q for q in [2, 3] for r in ['i', 'ii', 'iii']})
PAGES.update({('C', q, l, None): 16 + (q - 1) * 3 + {'a': 0, 'b': 0, 'c': 1, 'd': 2}[l]
              for q in range(1, 8) for l in 'abcd'})
PAGES.pop(('C', 7, 'a', None))
PAGES.update({('C', 7, 'a', r): 34 for r in ['i', 'ii']})


def question(doc, key):
    section, q, letter, roman = key
    value = page_text(doc, PAGES[key])
    if section in ['A', 'B']:
        value = re.split(r'Q\.\s*' + str(q) + r'\s+', value, maxsplit=1)[1]
        value = re.split(r'Q\.\s*\d+\s+', value, maxsplit=1)[0]
    else:
        value = select(value, '(' + letter + ')')
        value = re.split(r'(?<!part )\([abcd]\)\s+', value, maxsplit=1)[0]
    if roman:
        matches = list(re.finditer(r'(?<!part )\(' + roman + r'\)', value))
        assert len(matches) == 1, (key, value)
        value = value[matches[0].end():]
        value = re.split(r'(?<!part )\(i{1,3}\)\s+', value, maxsplit=1)[0]
    return tidy(re.sub(r'\(\d+\s+marks?\)', '', value))


def source(pages, kind='source-question', title='Original question'):
    return dict(kind=kind, label='OFFICIAL SOURCE', title=title, pages=pages,
                attribution='SEC LCVP Link Modules 2025 Common Level — © State Examinations Commission.',
                presentationNote='Read the complete original source and question in context.')


def paired_rows(count, labels, marks, guidance):
    rows = []
    for i in range(1, count + 1):
        row = criterion(f'profile-{i}', labels[0], 1, list(range(sum(marks) + 1)),
                        guidance if i == 1 else 'Use a different complete profile with its matching components.')
        row['parts'] = [dict(id=f'component-{j}', verbatim=label, marks=mark,
                             permittedMarks=list(range(mark + 1)))
                        for j, (label, mark) in enumerate(zip(labels, marks), 1)]
        rows.append(row)
    return rows


def challenge_cells(scheme):
    """Read each original table cell, never interleave its two columns."""
    page = scheme[13]
    headings = []
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            value = tidy(''.join(s['text'] for s in line['spans']))
            m = re.match(r'^([1-8])\.\s*(\S.*)', value)
            if m:
                headings.append((int(m[1]), line['bbox'], value))
    assert sorted(n for n, _, _ in headings) == list(range(1, 9)), headings
    headings.sort()
    # Require the original vertical table divider; do not guess from text positions.
    dividers = [item[1] for path in page.get_drawings() for item in path['items']
                if item[0] == 're' and item[1].width < 1 and item[1].height > 100
                and 200 < item[1].x0 < 400]
    vertical = [r.x0 for r in dividers]
    assert vertical, 'Original table divider missing from PDF geometry'
    split_x = min(vertical, key=lambda x: abs(x - page.rect.width / 2))
    row_bounds = sorted({(r.y0, r.y1) for r in dividers if abs(r.x0 - split_x) < .1})
    assert len(row_bounds) == 4
    cells = []
    for n, bbox, heading in headings:
        row_index = (n - 1) // 2
        upper, lower = row_bounds[row_index]
        clip = fitz.Rect(30 if n % 2 else split_x, upper,
                         split_x if n % 2 else page.rect.width - 25, lower)
        # Use glyph-span centres inside the ruled cell: font boxes can cross the
        # rule even when the visible text does not, so a clipped text page loses
        # headings or admits the preceding cell's final line.
        lines = []
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                spans = [s for s in line['spans'] if clip.contains(fitz.Point(
                    (s['bbox'][0] + s['bbox'][2]) / 2, (s['bbox'][1] + s['bbox'][3]) / 2))]
                if spans:
                    lines.append((line['bbox'][1], line['bbox'][0], ''.join(s['text'] for s in spans)))
        value = tidy(' '.join(t for _, _, t in sorted(lines)))
        assert value.startswith(str(n) + '.'), (n, clip, value)
        assert 'How to over come' in value, (n, value)
        cells.append(re.sub(r'^\d+\.\s*', '', value))
    assert len(cells) == 8
    return cells


def build():
    paper, scheme = documents()
    blocks = scheme_parts(scheme)
    rows, totals, topics = {}, {}, {}
    def put(key, mark, topic, value):
        rows[key], totals[key], topics[key] = value, mark, topic
    def a(n, r=None): return ('A', n, None, r)
    def b(n, r=None): return ('B', n, None, r)
    def c(n, l, r=None): return ('C', n, l, r)
    put(a(1), 1, '1-2', [point('manager-name', select(blocks[a(1)], '1 mark'), 1)])
    put(a(2), 2, '1-2', [criterion('whole-response', select(blocks[a(2)], '(0/2)'), 1, [0, 2],
        'Original whole-response allocation: 2 marks (0/2). No internal reason quota or 1-mark step is printed. '
        'Complete original models: ' + ' | '.join(numbered(blocks[a(2)], 2)))])
    put(a(3), 3, '1-2', menu(blocks[a(3)], 3, 1, 5))
    put(a(4), 2, '1-2', menu(blocks[a(4)], 2, 1, 5))
    put(a(5), 4, '1-2', partial(blocks[a(5)], 2, 2, 7))
    put(a(6, 'i'), 2, '1-4', menu(blocks[a(6, 'i')], 2, 1, 4))
    put(a(6, 'ii'), 4, '1-4', partial(blocks[a(6, 'ii')], 2, 2, 6))
    put(a(7), 6, '1-2', partial(blocks[a(7)], 3, 2, 6))
    put(a(8), 6, '1-2', partial(blocks[a(8)], 3, 2, 7))
    swot = split_heads(blocks[b(1)], r'\((i|ii|iii|iv)\)\s+', ['i', 'ii', 'iii', 'iv'])
    put(b(1), 6, '1-4', [point('swot-' + roman, value, note=(
        'Numeric scoring held: the source prints 6 marks (2+2+1+1) for the whole SWOT and requires '
        'ONE strength, ONE weakness, ONE opportunity and ONE threat. It does not label the category '
        'weights or prescribe best-two scoring. This is an allocation ambiguity, not an arithmetical '
        'contradiction. All four complete category pools remain visible; compare the whole response '
        'using confidence only pending authoritative clarification.' if roman == 'i' else ''))
        for roman, value in swot.items()])
    put(b(2, 'i'), 3, '1-3', menu(blocks[b(2, 'i')], 3, 1, 8))
    put(b(2, 'ii'), 6, '1-3', partial(blocks[b(2, 'ii')], 3, 2, 6))
    put(b(2, 'iii'), 3, '1-3', menu(blocks[b(2, 'iii')], 3, 1, 9))
    rows[b(2, 'iii')][0]['contextNote'] += ' All three reasons must support the ONE method chosen from your B2(ii) responses. No mark for naming the method is printed.'
    put(b(3, 'i'), 4, '1-3', partial(blocks[b(3, 'i')], 2, 2, 6))
    suggestion, scaffold = blocks[b(3, 'ii')].split('5 @ 1m')
    suggestions = numbered(suggestion, 9)
    put(b(3, 'ii'), 6, '1-3', [criterion('suggestion', 'Suggestion', 1, [0, 1],
        'Choose ONE specific suggestion and develop the same suggestion in the action plan. Original models: '
        + ' | '.join(suggestions)), criterion('action-plan-content', 'Action Plan', 5, [0, 1],
        'Five CONTENT points, 5 @ 1m; NO MARKS FOR HEADINGS. Original scaffold: '
        + ' | '.join(numbered(scaffold, 7)) + '. No completed model action plan is printed; none is invented.')])
    put(b(3, 'iii'), 2, '1-3', menu(blocks[b(3, 'iii')], 2, 1, 4))

    specs = [
        (1, 'a', 2, 2, 6, False, '1-4'), (1, 'b', 2, 2, 7, True, '1-4'),
        (1, 'd', 3, 3, 6, True, '1-4'), (2, 'b', 3, 2, 9, True, '0-1'),
        (2, 'c', 3, 2, 7, True, '0-2'), (3, 'a', 4, 1, 8, False, '0-4'),
        (3, 'b', 2, 2, 8, True, '0-0'), (3, 'c', 4, 2, 7, True, '0-0'),
        (3, 'd', 3, 3, 10, True, '0-0'), (4, 'c', 4, 2, 9, True, '1-1'),
        (5, 'b', 2, 2, 7, True, '1-3'), (5, 'c', 3, 3, 7, True, '1-3'),
        (5, 'd', 4, 2, 8, True, '1-3'), (6, 'a', 4, 1, 14, False, '1-1'),
        (6, 'b', 4, 1, 13, False, '1-4'), (6, 'd', 3, 3, 8, True, '1-1'),
        (7, 'b', 2, 2, 7, True, '0-0'), (7, 'c', 4, 2, 8, True, '0-0'),
        (7, 'd', 3, 3, 7, True, '0-0'),
    ]
    for q, letter, count, per, expected, has_partial, topic in specs:
        key = c(q, letter)
        put(key, count * per, topic, (partial if has_partial else menu)(blocks[key], count, per, expected))
    rows[c(3, 'd')][0]['contextNote'] += ' These figures and age qualifications are the original 2025 examination guidance; they have not been silently updated.'
    key = c(1, 'c')
    layout = select(blocks[key], 'Layout:', '3 @ 1 mark')
    labels = [tidy(v) for v in layout.split('/')]
    assert len(labels) == 3
    put(key, 8, '1-4', [point('layout-' + str(i), label, 1,
        'Required questionnaire layout component, 1 or 0. The source prints a grid, not a model questionnaire; no model is invented.' if i == 1 else '')
        for i, label in enumerate(labels, 1)] + [criterion('questions', '5 questions required', 5, [0, 1],
        'Five questions for the SAME local youth-facilities questionnaire, 1 mark each, in addition to all three layout components.')])
    key = c(2, 'a')
    put(key, 4, '0-2', paired_rows(2, ['Subject', 'Outline for this subject'], [1, 1],
        'Two different Leaving Certificate subjects you study; each subject name earns 1 mark and its matching '
        'outline of how it helped YOUR work experience earns 1 mark. Original allocation: '
        + select(blocks[key], '4 marks') + '. No prescribed subject pair or model personal response is printed.'))
    key = c(2, 'd')
    put(key, 9, '0-2', paired_rows(3, ['Source', 'Description', 'Reason'], [1, 1, 1],
        'THREE complete source + description + reason profiles. Original allocation: 3@3m (1+1+1). '
        'Keep the description and reason matched to the SAME source. Full original guidance: '
        + ' | '.join(numbered(blocks[key], 7))))
    key = c(4, 'a')
    put(key, 4, '1-1', [criterion('business', 'Name of the business', 1, [0, 2],
        'Name the business YOU visited, 2 or 0. The next required component must match this same business; no model business is invented.'),
        criterion('product-service', 'Product/Service it provides', 1, [0, 2],
        'Required product or service of that SAME business, 2 or 0. No internal 1-mark step is printed.')])
    key = c(4, 'b')
    put(key, 4, '1-1', [criterion('visit-content', 'Outline four key areas', 4, [0, 1],
        'Four CONTENT points from YOUR visit, 4 x 1 mark. The source explicitly states No marks for headings. '
        'These are the complete original scaffold areas, not paid label selections: '
        + ' | '.join(numbered(blocks[key], 11)))])
    key = c(4, 'd')
    put(key, 9, '1-1', paired_rows(3, ['Challenge description', 'Way(s) to overcome'], [1, 2],
        'THREE different complete challenge/solution profiles. Original allocation: Challenge description 1m; '
        'Way(s) to overcome 2m (1+1). Solutions must match the SAME challenge. Full original table, each cell kept intact: '
        + ' | '.join(f'{i}. {v}' for i, v in enumerate(challenge_cells(scheme), 1))))
    key = c(5, 'a')
    put(key, 4, '1-3', [point('agenda-heading', 'Heading (Agenda)', 1,
        'The required Agenda heading earns 1 mark; THREE agenda items earn 1 each. Do not add unprinted date, time or address marks.'),
        *menu(blocks[key], 3, 1, 10)])
    key = c(6, 'c')
    advantage = select(blocks[key], 'Advantages', 'Disadvantages')
    disadvantage = select(blocks[key], 'Disadvantages')
    put(key, 8, '1-1', [criterion('advantages', 'Advantages', 2, [0, 1, 2],
        'TWO advantages are required, each 2 marks (1+1); they cannot replace either required disadvantage. Complete original pool: '
        + ' | '.join(numbered(advantage, 5))), criterion('disadvantages', 'Disadvantages', 2, [0, 1, 2],
        'TWO disadvantages are required, each 2 marks (1+1); they cannot replace either required advantage. Complete original pool: '
        + ' | '.join(numbered(disadvantage, 8)))])
    key = c(7, 'a', 'i')
    put(key, 2, '0-0', [criterion('definition', select(blocks[key], 'A trade union is', include=True), 1, [0, 1, 2],
        'Explain the term using the complete original definition. Printed allocation: 2 marks (1+1); no required named union or invented internal quota.')])
    put(c(7, 'a', 'ii'), 2, '0-0', menu(blocks[c(7, 'a', 'ii')], 1, 2, 7))
    assert set(rows) == set(blocks) == set(PAGES), (set(blocks) - set(rows), set(rows) - set(blocks))

    case = select(page_text(paper, 9), 'Section B Case Study 30 marks')
    stems = {n: tidy(re.sub(r'^Q\.\s*\d+\s+25\s+marks\s*', '',
                           page_text(paper, 16 + (n - 1) * 3).split('(a)', 1)[0]))
             for n in range(1, 8)}
    cards = []
    for key in blocks:
        section, q, letter, roman = key
        suffix = section.lower() + str(q) + (letter or '') + (roman or '')
        ref = f'2025 CL Section {section} Q{q}' + (f'({letter})' if letter else '') + (f'({roman})' if roman else '')
        card = dict(id='lcvp-2025-cl-' + suffix, subjectId='lcvp', topicId='lcvp-link-modules-' + topics[key],
                    conceptId=concept_id('lcvp-2025-cl-' + suffix, suffix), level='common', year=2025, section=section, questionRef=ref,
                    questionText=question(paper, key), stem=stems[q] if section == 'C' else case if section == 'B' else '',
                    figureKey='', labelKey=[], totalMarks=totals[key], rows=rows[key],
                    tariffModel=dict(kind='questionTotal' if key == b(1) else 'fixed',
                        notation='Original 2025 allocation; complete source guidance retained'),
                    sourceMaterial=source([PAGES[key]]))
        if section == 'A':
            card['videoMaterial'] = dict(kind='source-video', label='OFFICIAL VIDEO', title='2025 LCVP audiovisual examination',
                playbackUrl=VIDEO_URL, canonicalUrl=VIDEO_URL, secFileid='LC462CLP031EV.mov',
                attribution='State Examinations Commission — original 2025 Common Level English audiovisual recording.',
                presentationNote='Watch the original charity-shop sequence with its sound before answering. The paper allows three minutes to read Section A, then the complete sequence, its three parts, and the complete sequence again. Use the original source link if embedded playback is unavailable.')
            card['additionalSourceMaterials'] = [source([3], title='Original audiovisual instructions')]
        elif section == 'B':
            card['sourceMaterial'] = source([9], 'source-text', 'Glenhale — complete case study')
            card['additionalSourceMaterials'] = [source([PAGES[key]])]
            if key == b(2, 'iii'):
                card['stem'] += ' ' + question(paper, b(2, 'ii'))
        elif key == c(1, 'd'):
            card['stem'] += ' ' + question(paper, c(1, 'c'))
            card['additionalSourceMaterials'] = [source([17], title='Original youth-facilities research context')]
        cards.append(card)
    assert len(cards) == 45 and sum(c['totalMarks'] for c in cards) == 235
    return cards, scheme


def write(cards, scheme):
    path = ROOT / 'scripts/markbank/authored/lcvp.json'
    old = json.loads(path.read_text())
    prior = [c for c in old if c['year'] == 2025]
    preserved = [c for c in old if c['year'] != 2025]
    assert len(preserved) == 316
    assert len(prior) in [42, 45]
    assert {c['id'] for c in prior} <= {c['id'] for c in cards}
    assert {c['id'] for c in cards} - {c['id'] for c in prior} in [set(),
        {'lcvp-2025-cl-a6ii', 'lcvp-2025-cl-c2a', 'lcvp-2025-cl-c4d'}]
    result = []
    inserted = False
    for card in old:
        if card['year'] == 2025:
            if not inserted:
                result.extend(cards)
                inserted = True
        else:
            result.append(card)
    assert [c for c in result if c['year'] != 2025] == preserved
    path.write_text(json.dumps(result, ensure_ascii=False, indent=1) + '\n')
    transcript = '# SEC LCVP 2025 Common Level written marking scheme\n\n'
    transcript += '\n\n'.join(f'## Physical page {i + 1}\n\n' + p.get_text(sort=True) for i, p in enumerate(scheme))
    (ROOT / 'examiner-reports/lcvp/schemes/2025-cl.md').write_text(transcript.rstrip() + '\n')
    review = json.loads(REVIEW.read_text())
    review['status'] = 'source-authored; independent-sweep-complete; one-numeric-allocation-hold'
    review['tasks'] = [dict(id=c['id'], questionRef=c['questionRef'], marks=c['totalMarks'], topicId=c['topicId']) for c in cards]
    review['heldNumericScoring'] = ['lcvp-2025-cl-b1']
    review['scoringScope'] = dict(printedOfferedMarks=235, pricedTaskMarks=229, heldWholeTaskMarks=6, heldTasks=1,
        distinction='All 45 source tasks (46 original leaves) are retained. The complete six-mark SWOT uses confidence-only review because the category allocation is unresolved. This is not a missing/excluded source task or a release-readiness claim.')
    review['legacyCorrections'] = dict(retainedStableIds=42,
        addedIds=['lcvp-2025-cl-a6ii', 'lcvp-2025-cl-c2a', 'lcvp-2025-cl-c4d'],
        guidance='Restore three omitted tasks, complete SWOT pools, B3(ii) suggestion mark and content-only plan, C1(c) eight-component questionnaire, C4(a) paired profile, C4(b) content-only credit, C5(a) Agenda heading mark, C6(c) two advantages AND two disadvantages, explicit partial ladders, required context and original video.')
    REVIEW.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    cards, scheme = build()
    if '--write' in sys.argv:
        write(cards, scheme)
    else:
        print(json.dumps(cards, ensure_ascii=False, indent=2))
