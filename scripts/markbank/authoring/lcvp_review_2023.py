#!/usr/bin/env python3
"""Original-source selectors after the independent 66-page 2023 main sweep."""
import hashlib
import json
import re
import sys
import fitz
from lcvp_review_2026 import ROOT, tidy, select, numbered, point, criterion, menu, partial
from lcvp_review_2025 import paired_rows
from lcvp_review_2024 import page_raw, split_raw

REVIEW = ROOT / 'scripts/markbank/authoring/lcvp/2023-cl-main-review.json'
PAPER = 'paper-trail-corpus/exampapers/2023/LC462CLP000EV.pdf'
SCHEME = 'paper-trail-corpus/markingschemes/2023/LC462CLP000EV.pdf'
HASHES = {PAPER: 'b14f72edc63c2909a24bc0dc116c823cf8910ddb17e00eccf7afb1cbcf26b492',
          SCHEME: '6e8b6ebb225d2da4f49034a547c37310bc2b775772f81c7b663636508d5aaa67'}
ADDED_IDS = {'lcvp-2023-cl-c6a', 'lcvp-2023-cl-c7b'}
VIDEO_URL = 'https://www.examinations.ie/archive/exampapers/2023/LC462CLP031EV.mov'


def documents():
    for path, expected in HASHES.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
    return fitz.open(ROOT / PAPER), fitz.open(ROOT / SCHEME)


def scheme_parts(doc):
    sections = split_raw('\n'.join(page_raw(doc, n) for n in range(4, 22)),
                         r'^\s*Section ([ABC])\s+', list('ABC'))
    out = {}
    for section, value in sections.items():
        questions = split_raw(value, r'^\s*Q\.\s*(\d+)\s*',
                              [str(n) for n in range(1, {'A': 8, 'B': 3, 'C': 7}[section] + 1)])
        for q, block in questions.items():
            if section == 'A' or (section == 'B' and q == '1'):
                out[(section, int(q), None, None)] = tidy(block)
            elif section == 'B':
                for roman, part in split_raw(block, r'^\s*\((i{1,3})\)\s*',
                                             ['i', 'ii'] if q == '2' else ['i', 'ii', 'iii']).items():
                    out[(section, int(q), None, roman)] = tidy(part)
            else:
                for letter, part in split_raw(block, r'^\s*\(([abcd])\)\s*', list('abcd')).items():
                    if (q, letter) == ('5', 'c'):
                        for roman, sub in split_raw(part, r'^\s*\((i{1,2})\)\s*', ['i', 'ii']).items():
                            out[(section, int(q), letter, roman)] = tidy(sub)
                    else:
                        out[(section, int(q), letter, None)] = tidy(part)
    assert len(out) == 43, len(out)
    return out


PAGES = {('A', q, None, None): p for q, p in enumerate([4, 4, 4, 5, 5, 6, 7, 8], 1)}
PAGES[('B', 1, None, None)] = 10
PAGES.update({('B', q, None, r): 9 + q for q, rs in [(2, ['i', 'ii']), (3, ['i', 'ii', 'iii'])] for r in rs})
PAGES.update({('C', q, l, None): 16 + (q - 1) * 3 + {'a': 0, 'b': 0, 'c': 1, 'd': 2}[l]
              for q in range(1, 8) for l in 'abcd'})
PAGES[('C', 7, 'b', None)] = 34
page = PAGES.pop(('C', 5, 'c', None))
PAGES.update({('C', 5, 'c', r): page for r in ['i', 'ii']})


def question(doc, key):
    section, q, letter, roman = key
    value = page_raw(doc, PAGES[key])
    if section in ['A', 'B']:
        value = re.split(r'^\s*Q\.\s*' + str(q) + r'\s+', value, maxsplit=1, flags=re.M)[1]
        value = re.split(r'^\s*Q\.\s*\d+\s+', value, maxsplit=1, flags=re.M)[0]
    else:
        value = re.split(r'^\s*\(' + letter + r'\)\s*', value, maxsplit=1, flags=re.M)[1]
        value = re.split(r'^\s*\([abcd]\)\s*', value, maxsplit=1, flags=re.M)[0]
    if roman:
        value = re.split(r'^\s*\(' + roman + r'\)\s*', value, maxsplit=1, flags=re.M)[1]
        value = re.split(r'^\s*\(i{1,3}\)\s*', value, maxsplit=1, flags=re.M)[0]
    return tidy(re.sub(r'\(\d+\s+marks?\)', '', value))


def source(pages, kind='source-question', title='Original question'):
    return dict(kind=kind, label='OFFICIAL SOURCE', title=title, pages=pages,
        attribution='SEC LCVP Link Modules 2023 Common Level — © State Examinations Commission.',
        presentationNote='Read the complete original source and question in context.')


def research_cells(doc):
    """Select literal characters from the two-column original ruled table."""
    page = doc[6]
    rules = [item[1] for path in page.get_drawings() for item in path['items']
             if item[0] == 're' and item[1].width < 1 and item[1].height > 5]
    xs = sorted({round(rect.x0, 2) for rect in rules})
    ys = sorted({(round(rect.y0, 2), round(rect.y1, 2)) for rect in rules if abs(rect.x0 - xs[0]) < .1})
    assert len(xs) == 3 and len(ys) == 2, (xs, ys)
    for x in xs:
        assert sorted({(round(r.y0, 2), round(r.y1, 2)) for r in rules if abs(r.x0 - x) < .1}) == ys
    rows = []
    for upper, lower in ys:
        row = []
        for left, right in zip(xs, xs[1:]):
            clip = fitz.Rect(left, upper, right, lower)
            lines = []
            for block in page.get_text('rawdict')['blocks']:
                for line in block.get('lines', []):
                    chars = [char for span in line['spans'] for char in span['chars']
                             if clip.contains(fitz.Point((char['bbox'][0] + char['bbox'][2]) / 2,
                                                         (char['bbox'][1] + char['bbox'][3]) / 2))]
                    if chars:
                        lines.append((line['bbox'][1], line['bbox'][0], ''.join(char['c'] for char in chars)))
            row.append(tidy(' '.join(value for _, _, value in sorted(lines))))
        rows.append(row)
    assert all(v for row in rows for v in row)
    return rows


def category_rows(block, first, second, counts, mark):
    """Preserve two compulsory categories plus one free third response."""
    pools = [select(block, first + ' 1.', second, include=True),
             select(block, second + ' 1.', include=True)]
    for pool, expected in zip(pools, counts):
        numbered(pool, expected)
    guidance = 'THREE different responses: one from EACH required category, then one other from EITHER category. No repetition. Complete original pools: ' + ' | '.join(pools)
    return [criterion('first-category', first, 1, list(range(mark + 1)), guidance),
            criterion('second-category', second, 1, list(range(mark + 1)), 'Required second category; it cannot be replaced by an extra response from the first category.'),
            criterion('other', 'one other', 1, list(range(mark + 1)), 'ONE further distinct response from either complete pool; do not repeat a point already claimed.')]


def build():
    paper, scheme = documents()
    blocks = scheme_parts(scheme)
    rows, totals, topics = {}, {}, {}
    def put(key, mark, topic, value):
        rows[key], totals[key], topics[key] = value, mark, topic
    def a(n): return ('A', n, None, None)
    def b(n, r=None): return ('B', n, None, r)
    def c(n, l, r=None): return ('C', n, l, r)
    put(a(1), 1, '0-2', [point('job', select(blocks[a(1)], '?', '1 mark'), 1)])
    for n, count, expected, topic in [(2, 2, 4, '0-2'), (3, 3, 6, '0-2'), (4, 2, 5, '0-1')]:
        put(a(n), count, topic, menu(blocks[a(n)], count, 1, expected))
    put(a(5), 4, '0-3', partial(blocks[a(5)], 2, 2, 4))
    notice = select(blocks[a(6)], 'Award 6 marks', '1.', include=True)
    put(a(6), 6, '0-3', [point('historical-award', notice, note=
        'The final scheme awarded SIX marks to ALL candidates for a misplaced question. This historical award is not an answer-dependent practice tariff. '
        'The same block also prints Three valid reasons beside 2 x 3 marks (0/3); neither is silently repaired. '
        'Compare the complete practice answer using confidence only. Automatic historical-award support is a separate follow-up; no default zero is called unassessed.')]
        + [point(f'model-{i}', value) for i, value in enumerate(numbered(select(blocks[a(6)], '1. Sending on', include=True), 8), 1)])
    put(a(7), 6, '0-0', partial(blocks[a(7)], 2, 3, 2,
        'TWO reasons, each with three content components (1+1+1). Both full examples and the any-relevant-stakeholder allowance remain visible.'))
    put(a(8), 6, '0-0', partial(blocks[a(8)], 3, 2, 7, 'State plus benefit; no repeated expansions.'))
    put(b(1), 6, '1-2', partial(blocks[b(1)], 3, 2, 7))
    put(b(2, 'i'), 3, '1-2', menu(blocks[b(2, 'i')], 3, 1, 10))
    put(b(2, 'ii'), 6, '0-0', category_rows(blocks[b(2, 'ii')], 'Advantages', 'Disadvantages', [10, 7], 2))
    cells = research_cells(scheme)
    research = []
    for i, expected in enumerate([7, 4]):
        models = numbered(cells[1][i], expected)
        row = criterion(f'research-{i + 1}', cells[0][i], 1, [0, 1, 2, 3],
            'TWO DIFFERENT types of research are required. This profile: type 1 + matching example 1 + relevant advantage 1. '
            'Do not repeat the advantage. Complete original example pool: ' + ' | '.join(models)
            + '. The source gives no completed model advantage; none is invented.')
        row['parts'] = [dict(id=label, verbatim=label, marks=1, permittedMarks=[0, 1]) for label in ['type', 'example', 'advantage']]
        research.append(row)
    put(b(3, 'i'), 6, '1-3', research)
    put(b(3, 'ii'), 6, '1-3', partial(blocks[b(3, 'ii')], 3, 2, 7,
        'No marks for headings. Each credited response needs valid content; areas already mentioned in the complete case are excluded by the original question.'))
    put(b(3, 'iii'), 3, '1-3', partial(blocks[b(3, 'iii')], 1, 3, 6, 'ONE statement and TWO matching expansions.'))

    specs = [(1, 'a', 2, 2, 9, '1-0'), (1, 'b', 3, 2, 6, '1-1'), (1, 'c', 3, 2, 10, '1-1'),
        (2, 'a', 2, 2, 7, '1-0'), (2, 'b', 3, 2, 9, '1-0'), (2, 'c', 3, 2, 7, '1-0'),
        (3, 'b', 3, 2, 16, '1-1'), (3, 'c', 3, 2, 8, '1-1'), (3, 'd', 3, 3, 8, '1-1'),
        (4, 'a', 2, 2, 8, '1-1'), (4, 'b', 2, 2, 6, '1-1'),
        (5, 'a', 2, 2, 11, '0-0'), (5, 'b', 3, 2, 14, '0-1'), (5, 'd', 3, 3, 15, '0-1'),
        (6, 'b', 3, 2, 7, '1-1'), (6, 'c', 3, 2, 5, '1-1'), (6, 'd', 3, 3, 6, '1-1'),
        (7, 'c', 3, 2, 7, '0-0'), (7, 'd', 4, 2, 13, '0-0')]
    for q, letter, count, per, expected, topic in specs:
        key = c(q, letter)
        put(key, count * per, topic, partial(blocks[key], count, per, expected))
    for key in [c(1, 'c'), c(3, 'c')]:
        rows[key][0]['contextNote'] += ' No repetition of expansions.'
    put(c(1, 'd'), 9, '1-1', category_rows(blocks[c(1, 'd')], 'Business', 'Consumers', [7, 6], 3))
    stages = ['Storming', 'Norming', 'Performing']
    put(c(2, 'd'), 9, '1-0', [criterion(f'stage-{i + 1}',
        select(blocks[c(2, 'd')], stage + ' –', stages[i + 1] + ' –' if i < 2 else None, include=True),
        1, [0, 1, 2, 3], 'This required stage: name and explanation, three content points (1+1+1). '
        'All THREE stages other than Forming are required; do not repeat Forming or substitute three points about one stage.')
        for i, stage in enumerate(stages)])
    put(c(3, 'a'), 4, '1-1', menu(blocks[c(3, 'a')], 4, 1, 11))
    ps = numbered(select(blocks[c(4, 'c')], '1. Product/service Name', include=True), 4)
    put(c(4, 'c'), 8, '1-1', [criterion(f'marketing-p-{i}', value.split(' ', 1)[0], 2, [0, 1],
        'TWO valid applications for this P to the SAME familiar business, 1 mark each. NO marks for headings. '
        'All FOUR Ps are required. Complete original application pool: ' + value) for i, value in enumerate(ps, 1)])
    put(c(4, 'd'), 9, '1-1', paired_rows(3, ['Method', 'Explanation of Method', 'reason of choosing Method'], [1, 1, 1],
        'THREE matched method/explanation/reason profiles. NO repetition of reasons. Complete original models: '
        + ' | '.join(numbered(blocks[c(4, 'd')], 8))))
    definition = select(blocks[c(5, 'c', 'i')], 'A legally binding agreement', include=True)
    phrases = [tidy(v) for v in definition.split('(1)') if tidy(v)]
    assert len(phrases) == 3
    put(c(5, 'c', 'i'), 3, '0-0', [point(f'definition-{i}', value, 1) for i, value in enumerate(phrases, 1)])
    put(c(5, 'c', 'ii'), 3, '0-0', menu(blocks[c(5, 'c', 'ii')], 3, 1, 13))
    put(c(6, 'a'), 4, '1-1', paired_rows(2, ['subject', 'operation of business'], [1, 1],
        'TWO subjects you study, each paired with how THAT subject helps you understand the operation of a business. '
        'Subject 1 + matching application 1. The source supplies criteria, not personal model answers; none is invented. Original guidance: '
        + select(blocks[c(6, 'a')], '1m for subject', include=True)))
    put(c(7, 'a'), 4, '1-1', [criterion('definition', select(blocks[c(7, 'a')], 'CSR stands', include=True), 4, [0, 1],
        'FOUR valid statements, 1 mark each, from the complete original explanation. No additional compulsory phrase or invented definition is imposed.')])
    put(c(7, 'b'), 7, '1-1', [point('enterprise', select(blocks[c(7, 'b')], '1m for enterprise', '3 X', include=True), 1,
        'Identify ONE enterprise with an active CSR policy, 1 mark. All three impacts must concern this SAME enterprise; the printed fast-food restaurant is illustrative.'),
        criterion('stakeholder-impacts', 'impacts on stakeholders', 3, [0, 1, 2],
        'THREE stakeholder impacts, statement + matching expansion, 1+1 each. Complete original models: '
        + select(blocks[c(7, 'b')], 'Customers –', include=True))])
    assert set(rows) == set(blocks) == set(PAGES)
    case = select(tidy(page_raw(paper, 9)), 'Section B Case Study 30 marks')
    stems = {n: tidy(re.sub(r'^Q\.\s*\d+\s+25\s+marks\s*', '',
        page_raw(paper, 16 + (n - 1) * 3).split('(a)', 1)[0])) for n in range(1, 8)}
    cards = []
    for key in blocks:
        section, q, letter, roman = key
        suffix = section.lower() + str(q) + (letter or '') + (roman or '')
        ref = f'2023 CL Section {section} Q{q}' + (f'({letter})' if letter else '') + (f'({roman})' if roman else '')
        card = dict(id='lcvp-2023-cl-' + suffix, subjectId='lcvp', topicId='lcvp-link-modules-' + topics[key],
            conceptId=suffix, level='common', year=2023, section=section, questionRef=ref,
            questionText=question(paper, key), stem=stems[q] if section == 'C' else case if section == 'B' else '',
            figureKey='', labelKey=[], totalMarks=totals[key], rows=rows[key],
            tariffModel=dict(kind='questionTotal' if key == a(6) else 'fixed',
                             notation='Original 2023 allocation; historical universal award retained for A6'),
            sourceMaterial=source([PAGES[key]]))
        if section == 'A':
            card['videoMaterial'] = dict(kind='source-video', label='OFFICIAL VIDEO', title='2023 LCVP audiovisual examination',
                playbackUrl=VIDEO_URL, canonicalUrl=VIDEO_URL, secFileid='LC462CLP031EV.mov',
                attribution='State Examinations Commission — original 2023 Common Level English audiovisual recording.',
                presentationNote='Watch the original Career Investigation sequence with its sound before answering. Follow the original printed viewing instructions. Use the original source link if embedded playback is unavailable.')
            card['additionalSourceMaterials'] = [source([3], title='Original audiovisual instructions')]
        elif section == 'B':
            card['sourceMaterial'] = source([9], 'source-text', 'Ballyfert — complete case study')
            card['additionalSourceMaterials'] = [source([PAGES[key]])]
        cards.append(card)
    assert len(cards) == 43 and sum(card['totalMarks'] for card in cards) == 235
    return cards, scheme


def write(cards, scheme):
    path = ROOT / 'scripts/markbank/authored/lcvp.json'
    old = json.loads(path.read_text())
    prior = [c for c in old if c['year'] == 2023]
    preserved = [c for c in old if c['year'] != 2023]
    assert len(preserved) == 326 and len(prior) in [41, 43]
    assert {c['id'] for c in prior} <= {c['id'] for c in cards}
    assert {c['id'] for c in cards} - {c['id'] for c in prior} in [set(), ADDED_IDS]
    result, inserted = [], False
    for card in old:
        if card['year'] == 2023:
            if not inserted:
                result.extend(cards)
                inserted = True
        else:
            result.append(card)
    assert [c for c in result if c['year'] != 2023] == preserved
    path.write_text(json.dumps(result, ensure_ascii=False, indent=1) + '\n')
    transcript = '# SEC LCVP 2023 Common Level written marking scheme\n\n'
    pages = []
    for i, page in enumerate(scheme, 1):
        value = f'## Physical page {i}\n\n' + page.get_text(sort=True)
        if i == 7:
            value += '\n\n### Original ruled table — character-centre cell order\n\n'
            value += '\n'.join(' | '.join(row).rstrip() for row in research_cells(scheme))
        pages.append(value)
    transcript += '\n\n'.join(pages)
    (ROOT / 'examiner-reports/lcvp/schemes/2023-cl.md').write_text(transcript.rstrip() + '\n')
    review = json.loads(REVIEW.read_text())
    review['status'] = 'source-authored; independent-sweep-complete; validation-pending'
    review['tasks'] = [dict(id=c['id'], questionRef=c['questionRef'], marks=c['totalMarks'], topicId=c['topicId']) for c in cards]
    review['legacyCorrections'] = dict(retainedStableIds=41, addedIds=sorted(ADDED_IDS),
        previousPrintedMarks=224, correctedPrintedMarks=235,
        canonicalTopics='Reviewed against curriculumRegistry.ts; old metadata corrected without changing any old ID or concept. Original Atlas assessment-format anchors preserved.')
    review['heldNumericScoring'] = [dict(task='A6', printedMarks=6,
        reason='Historical universal six-mark award for a misplaced question; not an answer-dependent practice allocation. Complete source notice and eight models retained unpriced.',
        practiceMode='questionTotal confidence review; shared automatic historical-award support is a later root follow-up')]
    review['numericSourceAmbiguities'][0]['practiceTreatment'] = 'Whole-task questionTotal confidence review confirmed by root; universal-award contract does not yet exist. No answer-dependent controls.'
    REVIEW.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    cards, scheme = build()
    if '--write' in sys.argv:
        write(cards, scheme)
    else:
        print(json.dumps(cards, ensure_ascii=False, indent=2))
