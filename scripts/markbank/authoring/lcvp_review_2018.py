#!/usr/bin/env python3
"""Source selectors following the independent 56-page 2018 visual review."""
import hashlib
import json
import re
import sys
import fitz
from lcvp_review_2026 import ROOT, tidy, select, point, criterion
from lcvp_review_2025 import paired_rows
from lcvp_review_2024 import split_raw
from lcvp_review_2022 import page_raw
from lcvp_identity import concept_id

REVIEW = ROOT / 'scripts/markbank/authoring/lcvp/2018-cl-main-review.json'
PAPER = 'paper-trail-corpus/exampapers/2018/LC462CLP000EV.pdf'
SCHEME = 'paper-trail-corpus/markingschemes/2018/LC462CLP000EV.pdf'
HASHES = {PAPER: '3e7b2a2c14343b958d854641b637afca191a22ba6ae674e7d0fcfc81cd9c1276',
          SCHEME: '90aa2988c3fb84ca6fcea3ee15a371cb77b9b97da18ee1aad7dd3838c3ad7006'}
VIDEO_URL = 'https://www.examinations.ie/archive/exampapers/2018/LC462CLP031EV.mp4'
ADDED_IDS = {'lcvp-2018-cl-' + s for s in ['b3i', 'c1c', 'c2a', 'c2bii', 'c2d', 'c4aii', 'c6b', 'c6d']}


def documents():
    for path, expected in HASHES.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
    return fitz.open(ROOT / PAPER), fitz.open(ROOT / SCHEME)


def paper_raw(doc, number):
    """Remove only exact furniture spans at their original page coordinates.

    C5's real stem extends into the margin: a rectangular right-edge crop
    would truncate it. Retain every other span, including that full stem.
    """
    page = doc[number - 1]
    lines = []
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            kept = []
            for span in line['spans']:
                value, box = tidy(span['text']), fitz.Rect(span['bbox'])
                examiner = value in ['Examiner', 'only'] and box.x0 > 530 and box.y1 < 90
                totals = value in ['page', 'running'] and box.x0 > 480 and box.y0 > 760
                named_footer = value in ['Leaving Certificate Vocational Programme', 'Link Modules Examination 2018'] and box.y0 > page.rect.height * .82
                numeric_footer = re.fullmatch(r'\d{1,2}', value) and box.y0 > page.rect.height * .9 and .4 * page.rect.width < (box.x0 + box.x1) / 2 < .6 * page.rect.width
                if not (examiner or totals or named_footer or numeric_footer):
                    kept.append(span['text'])
            if tidy(''.join(kept)):
                lines.append((line['bbox'][1], line['bbox'][0], ''.join(kept)))
    return '\n'.join(value for _, _, value in sorted(lines))


def header_body(raw):
    mark = re.search(r'\b\d+\s+[Mm]arks?\b', raw)
    assert mark, raw[:180]
    return raw[:mark.end()], raw[mark.end():]


def scheme_parts(doc):
    sections = split_raw('\n'.join(page_raw(doc, n) for n in range(4, 20)),
                         r'^\s*Section ([ABC])\s+', list('ABC'))
    out = {}
    for section, value in sections.items():
        questions = split_raw(value, r'^\s*Q\.?\s*(\d+)\s*',
                              [str(n) for n in range(1, {'A': 8, 'B': 3, 'C': 6}[section] + 1)])
        for q, block in questions.items():
            q = int(q)
            if section == 'A' or (section == 'B' and q == 1):
                out[(section, q, None, None)] = block
            elif section == 'B':
                heading, body = header_body(block)
                if q == 2:
                    parts = split_raw(body, r'^\s*\((i{1,2})\)\s*', ['i', 'ii'])
                else:
                    marker = list(re.finditer(r'^\s*\(ii\)\s*', body, re.M))
                    assert len(marker) == 1
                    parts = {'i': body[:marker[0].start()], 'ii': body[marker[0].end():]}
                for roman, part in parts.items():
                    out[(section, q, None, roman)] = heading + '\n' + part
            else:
                for letter, part in split_raw(block, r'^\s*\(([abcd])\)\s*', list('abcd')).items():
                    if (q, letter) in [(2, 'b'), (4, 'a')]:
                        heading, body = header_body(part)
                        for roman, sub in split_raw(body, r'^\s*\((i{1,2})\)\s*', ['i', 'ii']).items():
                            out[(section, q, letter, roman)] = heading + '\n' + sub
                    elif (q, letter) == (1, 'b'):
                        heading, body = header_body(part)
                        parts = split_raw(body, r'^\s*(Household|Local Community)\s*$', ['Household', 'Local Community'])
                        for roman, title in [('i', 'Household'), ('ii', 'Local Community')]:
                            out[(section, q, letter, roman)] = heading + '\n' + title + '\n' + parts[title]
                    else:
                        out[(section, q, letter, None)] = part
    return out


def before_rate(raw, pattern):
    matches = list(re.finditer(pattern, raw))
    assert len(matches) == 1, (pattern, len(matches), raw)
    return raw[:matches[0].start()]


def models(raw, count, first=1):
    """Keep printed lines; A2 lacks spaces after dots and A4 omits two dots."""
    matches = list(re.finditer(r'^\s*(\d{1,2})\.?\s*(?=[A-Za-zÀ-ž])', raw, re.M))
    assert [int(m[1]) for m in matches] == list(range(first, first + count)), (first, count, raw)
    result = [tidy(raw[m.end():matches[i + 1].start() if i + 1 < len(matches) else len(raw)])
              for i, m in enumerate(matches)]
    result[-1] = re.sub(r'\s+RP$', '', result[-1]).strip()
    assert all(result)
    return result


def response_row(key, label, pool, count, steps, guidance=''):
    return criterion(key, label, count, steps,
        guidance + ' Keep each response distinct and credit it only once. Complete original guidance: ' + ' | '.join(pool))


def choice_row(key, label, pool, count, per, guidance='', steps=None):
    group = dict(claimMax=count, perOption=per, options=pool)
    if steps is not None:
        assert len(steps) == count
        group['perOptionSteps'] = steps
    return dict(id=key, kind='anyN', verbatim=tidy(label), marks=sum(steps) if steps else count * per,
                openList=True, group=group, contextNote=guidance)


PAGES = {('A', q, None, None): p for q, p in enumerate([4, 4, 4, 5, 5, 6, 7, 8], 1)}
PAGES[('B', 1, None, None)] = 10
PAGES.update({('B', q, None, r): 9 + q for q in [2, 3] for r in ['i', 'ii']})
PAGES.update({('C', q, l, None): 16 + (q - 1) * 3 + {'a': 0, 'b': 0, 'c': 1, 'd': 2}[l]
              for q in range(1, 7) for l in 'abcd'})
for q, letter in [(1, 'b'), (2, 'b'), (4, 'a')]:
    page = PAGES.pop(('C', q, letter, None))
    PAGES.update({('C', q, letter, r): page for r in ['i', 'ii']})


def question(doc, key):
    section, q, letter, roman = key
    value = paper_raw(doc, PAGES[key])
    if section in ['A', 'B']:
        value = re.split(r'^\s*Q\.\s*' + str(q) + r'\s+', value, maxsplit=1, flags=re.M)[1]
        value = re.split(r'^\s*Q\.\s*\d+\s+', value, maxsplit=1, flags=re.M)[0]
    else:
        value = re.split(r'^\s*\(' + letter + r'\)\s*', value, maxsplit=1, flags=re.M)[1]
        value = re.split(r'^\s*\([abcd]\)\s*', value, maxsplit=1, flags=re.M)[0]
    if roman:
        value = re.split(r'\(' + roman + r'\)\s*', value, maxsplit=1)[1]
        value = re.split(r'\(i{1,3}\)\s*', value, maxsplit=1)[0]
    return tidy(re.sub(r'\(\d+\s+marks?\)', '', value))


def source(pages, kind='source-question', title='Original question'):
    return dict(kind=kind, label='OFFICIAL SOURCE', title=title, pages=pages,
                attribution='SEC LCVP Link Modules 2018 Common Level — © State Examinations Commission.',
                presentationNote='Read the complete original source and question in context.')


def build_ab(paper, scheme):
    raw = scheme_parts(scheme)
    rows, totals, topics = {}, {}, {}
    def put(key, marks, topic, value):
        rows[key], totals[key], topics[key] = value, marks, topic
    def a(q): return ('A', q, None, None)
    def b(q, roman=None): return ('B', q, None, roman)
    def labelled(key):
        header, body = header_body(raw[key])
        return tidy(re.sub(r'\b\d+\s+[Mm]arks?\b', '', header)), body

    _, body = labelled(a(1))
    put(a(1), 1, '1-1', [point('business', tidy(body), 1)])
    for q, count, per, expected, rate in [
        (2, 2, 1, 3, r'Any\s*2\s*@\s*1m'),
        (3, 3, 1, 4, r'3\s*@\s*1m'),
        (4, 2, 2, 3, r'2\s*@\s*2m\(0/2\)'),
        (5, 4, 1, 5, r'4\s*@\s*1\s*mark'),
    ]:
        label, body = labelled(a(q))
        pool = models(before_rate(body, rate), expected)
        put(a(q), count * per, '1-1', [choice_row('responses', label, pool, count, per,
            f'Choose {count} distinct original responses. Each receives {per} or 0 marks; no unprinted partial award is introduced.')])
    for q, count, expected, rate in [(6, 2, 4, r'2\s*@\s*2m\(1\+1\)'), (7, 3, 6, r'3\s*@\s*2m\s*\(1\+1\)')]:
        label, body = labelled(a(q))
        put(a(q), count * 2, '1-1', [response_row('responses', label,
            models(before_rate(body, rate), expected), count, [0, 1, 2],
            f'Original allocation: {count} responses at 2 marks (1+1).')])
    _, body = labelled(a(8))
    parts = split_raw(body, r'^\s*Question\s+([12])\s*$', ['1', '2'])
    first = models(before_rate(parts['1'], r'\(2\s*@\s*1\)'), 2)
    second = models(before_rate(parts['2'], r'2\s*@\s*2\(1\+1\)\)'), 4, first=3)
    put(a(8), 6, '1-1', [
        choice_row('question-1', 'Question 1', first, 2, 1,
                   'Both original questions are required. First question: two answers at 1 mark each.'),
        response_row('question-2', 'Question 2', second, 2, [0, 1, 2],
                     'Second question: two responses at 2 marks (1+1); retain the separate first-question allocation.')])

    label, body = labelled(b(1))
    definitions = split_raw(before_rate(body, r'3\s*@\s*2m\(0/2\)'),
                            r'^\s*\((i|ii|iii|iv)\)\s*', ['i', 'ii', 'iii', 'iv'])
    put(b(1), 6, '1-2', [choice_row('terms', label, [tidy(v) for v in definitions.values()], 3, 2,
        'Choose THREE of all FOUR printed terms. Each definition receives 2 or 0 marks, exactly as printed. Keep the full original definition pool; no partial 1 mark is printed.')])
    _, body = labelled(b(2, 'i'))
    influences, gains = body.split('What might Tommy gain from volunteering.', 1)
    first = models(before_rate(influences, r'4\s*@\s*1m\s+each'), 6)
    second = models(before_rate(gains, r'4\s*@\s*1m\s+each'), 6, first=7)
    put(b(2, 'i'), 8, '1-2', [
        choice_row('influences', 'Influences on where to volunteer.', first, 4, 1,
            'FOUR influences, 1 mark each, and FOUR gains, 1 mark each. Both components are required; retain the whole Tommy/Sarah case.'),
        choice_row('gains', 'What might Tommy gain from volunteering.', second, 4, 1,
            'FOUR distinct gains, 1 mark each; keep the separately required influences above.')])
    _, body = labelled(b(2, 'ii'))
    put(b(2, 'ii'), 4, '1-2', [choice_row('steps',
        tidy(body.split('1.', 1)[0]), models(before_rate(body, r'4\s*@\s*1m\s+each'), 9), 4, 1,
        'FOUR distinct recruitment steps, 1 mark each; all nine original models remain available.')])
    label, body = labelled(b(3, 'i'))
    label = tidy(label.split('(i)', 1)[1].split('(ii)', 1)[0])
    compare, contrast = body.split('CONTRAST:', 1)
    first = models(compare, 4)
    second = models(before_rate(contrast, r'6\s*@\s*1m'), 7, first=5)
    full = 'COMPARE: ' + ' | '.join(first) + ' CONTRAST: ' + ' | '.join(second)
    put(b(3, 'i'), 6, '1-2', [
        response_row('compare', 'COMPARE:', first, 2, [0, 1],
            'Original rule: 6@1m; A minimum of 2 in each area. Credit TWO compare points here, TWO contrast points below, then TWO further DISTINCT points from either category. A point can be credited only once across all six slots. Complete original pools: ' + full),
        response_row('contrast', 'CONTRAST:', second, 2, [0, 1],
            'TWO distinct contrast points. Do not reuse points credited in any other row.'),
        response_row('further', label, first + second, 2, [0, 1],
            'TWO further distinct points from either category, not already credited. This preserves 2+4, 3+3 or 4+2; no fixed 3+3 split.')])
    _, body = labelled(b(3, 'ii'))
    put(b(3, 'ii'), 6, '1-2', [choice_row('challenges', tidy(body.split('1.', 1)[0]),
        models(before_rate(body, r'3\s*@\s*2m\(0/2\)'), 8), 3, 2,
        'THREE distinct challenges, each 2 or 0 marks; the original scheme gives no 1-mark partial step.')])
    assert len(rows) == 13 and sum(totals.values()) == 60
    return rows, totals, topics, raw


def build():
    paper, scheme = documents()
    rows, totals, topics, raw = build_ab(paper, scheme)
    def c(q, letter, roman=None): return ('C', q, letter, roman)
    def put(key, marks, topic, value):
        rows[key], totals[key], topics[key] = value, marks, topic
    def labelled(key):
        header, body = header_body(raw[key])
        return tidy(re.sub(r'\b\d+\s+[Mm]arks?\b', '', header)), body
    def ordinary(key, topic, count, per, expected, rate, binary=False):
        label, body = labelled(key)
        pool = models(before_rate(body, rate), expected)
        if binary or per == 1:
            value = choice_row('responses', label, pool, count, per,
                f'Choose {count} distinct relevant responses. Each receives {per} or 0 marks; preserve every original alternative.')
        else:
            value = response_row('responses', label, pool, count, list(range(per + 1)),
                f'Original allocation: {count} responses at {per} marks, with each printed 1-mark component retained.')
        put(key, count * per, topic, [value])

    label, body = labelled(c(1, 'a'))
    put(c(1, 'a'), 4, '1-0', [response_row('definition', label,
        [tidy(before_rate(body, r'2\s*@\s*2m\(0/2\)'))], 2, [0, 2],
        'Original two components at 2 or 0 marks each. Keep the complete definition; no compulsory semantic split or 1-mark step is invented.')])
    for roman, title, expected, topic in [('i', 'Household', 6, '1-0'), ('ii', 'Local Community', 5, '1-2')]:
        _, body = labelled(c(1, 'b', roman))
        put(c(1, 'b', roman), 2, topic, [choice_row('examples', title,
            models(before_rate(body, r'2\s*@\s*1m'), expected), 2, 1,
            'TWO examples in this printed roman context, 1 mark each. The source also prints RP. Keep the parent instruction and the separately priced companion context.')])
    _, body = labelled(c(1, 'c'))
    agencies = models(body, 12)
    put(c(1, 'c'), 8, '1-1', paired_rows(2, ['Name of agency', 'Type of support'], [1, 3],
        'TWO distinct agencies: each name 1, its matching support 3 (1+1+1). Keep each support linked to the SAME agency. All twelve source profiles, including agencies for which no detailed support model is printed: ' + ' | '.join(agencies)))
    _, body = labelled(c(1, 'd'))
    heads = ['Planning', 'Good managerial skills', 'Product development']
    pools = split_raw(body, r'^\s*(Planning|Good managerial skills|Product development):\s*$', heads)
    put(c(1, 'd'), 9, '1-0', [choice_row(title.lower().replace(' ', '-'), title + ':',
        models(before_rate(pools[title], r'3\s*@\s*1m'), count), 3, 1,
        'All THREE printed headings are required. Give three relevant points under this heading, 1 each; keep every original model.')
        for title, count in zip(heads, [8, 8, 4])])
    put(c(2, 'a'), 3, '0-2', [point('career', 'Name of career', 1),
        criterion('skills', 'Skills/qualities appropriate to the career', 2, [0, 1],
            'TWO skills/qualities appropriate to the SAME named career, 1 each. The original scheme supplies criteria, not a personal model; none is invented.')])
    ordinary(c(2, 'b', 'i'), '0-3', 2, 1, 8, r'2\s*@\s*1m')
    _, method_body = labelled(c(2, 'b', 'i'))
    rows[c(2, 'b', 'i')][0]['verbatim'] = tidy(method_body.split('1.', 1)[0])
    _, body = labelled(c(2, 'b', 'ii'))
    pool = models(before_rate(body, r'RP\s+Any\s+2\s+relevant\s+points\s+given'), 5)
    put(c(2, 'b', 'ii'), 3, '0-3', [choice_row('advantages',
        'Any two advantages related to one of the methods mentioned above', pool, 2, 2,
        'Both advantages must relate to ONE of the methods named in part(i). Original allocation: Any 2 relevant points given; 2m, 1m. Retain this unequal two-answer award and the source RP instruction; do not divide the marks equally.', steps=[2, 1])])
    ordinary(c(2, 'c'), '0-0', 3, 3, 7, r'3\s*@\s*3m\(1\+1\+1\)')
    label, body = labelled(c(2, 'd'))
    first, second = body.split('Two Career Paths-2 routes to same profession', 1)
    assert re.fullmatch(r'\s*2\s*@\s*2m\s*\(1\+1\)\s*', second)
    put(c(2, 'd'), 8, '0-2', [
        response_row('evaluation', label, models(before_rate(first, r'2\s*@\s*2m\s*\(1\+1\)'), 5), 2, [0, 1, 2],
            'The original scheme explicitly prices this task at 8 although the actual paper page omits its individual tariff. Two influence/evaluation responses, 2 marks (1+1) each.'),
        criterion('career-paths', 'Two Career Paths-2 routes to same profession', 2, [0, 1, 2],
            'The separately printed two career-path responses receive 2 (1+1) each. Preserve the source allowance for two routes to the SAME profession; do not require two different professions.')])
    put(c(3, 'a'), 2, '1-1', [criterion('workplaces', 'Any two workplaces named @ 1 mark each', 2, [0, 1],
        'Name TWO workplaces in the local area. No local personal examples are printed or invented.')])
    _, body = labelled(c(3, 'b'))
    swot = split_raw(before_rate(body, r'4\s*@\s*2m\(1/1\)'),
                     r'^\s*(Strengths|Weaknesses|Opportunities|Threats):\s*', ['Strengths', 'Weaknesses', 'Opportunities', 'Threats'])
    values = []
    for index, (heading, expected) in enumerate(zip(swot, [5, 3, 4, 5])):
        pool = [tidy(line) for line in swot[heading].splitlines() if line.strip()]
        assert len(pool) == expected, (heading, pool)
        note = ('Across the whole SWOT answer, retain the exact source instructions: 4@2m(1/1); 2 points under each heading; 1 specific point to tidy towns; No marks for headings; No repetition of points. '
                if index == 0 else 'Two relevant points under this heading, 1 each. No repeated points or marks for writing the heading. ')
        values.append(response_row(heading.lower(), heading + ':', pool, 2, [0, 1], note))
    put(c(3, 'b'), 8, '1-2', values)
    ordinary(c(3, 'c'), '1-2', 6, 1, 10, r'6\s*@\s*1m')
    ordinary(c(3, 'd'), '1-2', 3, 3, 5, r'3\s*@\s*3m\(1\+1\+1\)')
    _, body = labelled(c(4, 'a', 'i'))
    unions = select(tidy(body), 'eg:', '2@1m').split('/')
    assert len(unions) == 8
    put(c(4, 'a', 'i'), 2, '0-0', [choice_row('unions', 'Name any two trade unions', unions, 2, 1,
        'TWO union names, 1 each. All eight original examples and their historical spellings are retained.')])
    _, body = labelled(c(4, 'a', 'ii'))
    put(c(4, 'a', 'ii'), 3, '0-0', [point('definition', select(tidy(body), 'A shop steward', '3m', include=True), 3,
        'The complete original definition is allocated 3 marks. No internal partial ladder is printed or invented.')])
    ordinary(c(4, 'b'), '0-0', 4, 2, 8, r'4\s*@\s*2m\(1\+1\)')
    _, body = labelled(c(4, 'c'))
    first, second = body.split('Affect of poor Industrial relations.', 1)
    put(c(4, 'c'), 6, '0-0', [
        choice_row('benefits', 'Benefits:', models(before_rate(first, r'3\s*@\s*1m'), 6), 3, 1,
            'Both questions are required: three benefits of good relations, 1 each, and three effects of poor relations, 1 each.'),
        choice_row('poor-effects', 'Affect of poor Industrial relations.', models(before_rate(second, r'3\s*@\s*1m'), 7, first=7), 3, 1,
            'THREE distinct effects of poor relations, 1 each, beside the separately required benefits.')])
    ordinary(c(4, 'd'), '0-0', 3, 2, 8, r'3\s*@\s*2m\(1\+1\)')
    ordinary(c(5, 'a'), '1-0', 2, 2, 9, r'2\s*@\s*2m\(0/2\)', binary=True)
    ordinary(c(5, 'b'), '1-0', 3, 2, 8, r'3\s*@\s*2m\(1\+1\)')
    ordinary(c(5, 'c'), '1-0', 3, 2, 9, r'3\s*@\s*2m\s*\(1\+1\)')
    ordinary(c(5, 'd'), '1-3', 3, 3, 7, r'3\s*@\s*3m\(1\+1\+1\)')
    ordinary(c(6, 'a'), '1-3', 3, 1, 8, r'3\s*@\s*1m')
    _, body = labelled(c(6, 'b'))
    definition = tidy(before_rate(body, r'(?m)^\s*1m\s*/'))
    fragments = [tidy(v) for v in definition.split('/')]
    assert len(fragments) == 4 and fragments[3] == 'service', fragments
    middle = re.split(r',\s*|\s+and\s+', fragments[1])
    assert middle == ['Product', 'Price', 'Place', 'Promotion']
    purpose = fragments[2] + '/' + fragments[3]
    put(c(6, 'b'), 6, '1-3', [point('combination', fragments[0], 1),
        *[point('mix-' + v.lower(), v, 1) for v in middle], point('purpose', purpose, 1,
            'Original definition allocation: combination 1; Product, Price, Place and Promotion 4×1; purpose 1. All components are required.')])
    _, body = labelled(c(6, 'c'))
    pool = models(before_rate(body, r'2\s+points\s+under\s+each\s+heading'), 5)
    put(c(6, 'c'), 8, '1-3', [point(f'model-{i}', value, note=(
        'Numeric scoring held. Original source lists FIVE headings, then “2 points under each heading”, “No marks for headings” and “4@2(1+1)”, with total 8. All five headings and the full task remain; confidence review only pending authoritative clarification. No choose-four rule, removed research heading, repaired total or partial allocation is inferred.' if i == 1 else '')) for i, value in enumerate(pool, 1)])
    ordinary(c(6, 'd'), '1-0', 4, 2, 7, r'4\s*@\s*2\(1\+1\)m')
    assert set(rows) == set(raw) == set(PAGES)
    assert len(rows) == 40 and sum(totals.values()) == 210

    case = select(tidy(paper_raw(paper, 9)), 'Section B Case Study 30 marks')
    stems = {q: tidy(re.sub(r'^\s*Q\.\s*\d+\s*|\(25\s+marks\)', '',
                           paper_raw(paper, 16 + (q - 1) * 3).split('(a)', 1)[0])) for q in range(1, 7)}
    cards = []
    for key in raw:
        section, q, letter, roman = key
        suffix = section.lower() + str(q) + (letter or '') + (roman or '')
        card_id = 'lcvp-2018-cl-' + suffix
        ref = f'2018 CL Section {section} Q{q}' + (f'({letter})' if letter else '') + (f'({roman})' if roman else '')
        card = dict(id=card_id, subjectId='lcvp', topicId='lcvp-link-modules-' + topics[key],
                    conceptId=concept_id(card_id, suffix), level='common', year=2018, section=section,
                    questionRef=ref, questionText=question(paper, key),
                    stem=stems[q] if section == 'C' else case if section == 'B' else '', figureKey='', labelKey=[],
                    totalMarks=totals[key], rows=rows[key], tariffModel=dict(kind='questionTotal' if key == c(6, 'c') else 'fixed',
                        notation='Original 2018 marking scheme allocation.'), sourceMaterial=source([PAGES[key]]))
        if section == 'A':
            card['videoMaterial'] = dict(kind='source-video', label='OFFICIAL VIDEO', title='2018 LCVP audiovisual examination',
                playbackUrl=VIDEO_URL, canonicalUrl=VIDEO_URL, secFileid='LC462CLP031EV.mp4',
                attribution='State Examinations Commission — original 2018 Common Level English audiovisual recording.',
                presentationNote='Watch the original Business Location sequence with its sound before answering. Follow the printed viewing instructions. Use the original source link if embedded playback is unavailable.')
            card['additionalSourceMaterials'] = [source([3], title='Original audiovisual instructions')]
        elif section == 'B':
            card['sourceMaterial'] = source([9], 'source-text', 'Volunteering — complete case study')
            card['additionalSourceMaterials'] = [source([PAGES[key]])]
        if key in [c(1, 'b', 'i'), c(1, 'b', 'ii')]:
            card['stem'] += ' ' + select(tidy(paper_raw(paper, 16)), '(b)', '(i)')
        if key == c(2, 'b', 'ii'):
            card['stem'] += ' ' + question(paper, c(2, 'b', 'i'))
        cards.append(card)
    return cards, scheme


def write(cards, scheme):
    review = json.loads(REVIEW.read_text())
    assert review['manualPricedTasks'] == 40, 'Finish the C1(b) source/preservation boundary review before writes'
    path = ROOT / 'scripts/markbank/authored/lcvp.json'
    old = json.loads(path.read_text())
    prior = [c for c in old if c['year'] == 2018]
    preserved = [c for c in old if c['year'] != 2018]
    assert len(prior) in [32, 40] and len(preserved) == 358
    assert {c['id'] for c in prior} <= {c['id'] for c in cards}
    assert {c['id'] for c in cards} - {c['id'] for c in prior} in [set(), ADDED_IDS]
    concepts = {c['id']: c['conceptId'] for c in prior}
    assert all(c['conceptId'] == concepts.get(c['id'], c['conceptId']) for c in cards)
    result, inserted = [], False
    for card in old:
        if card['year'] == 2018:
            if not inserted:
                result.extend(cards)
                inserted = True
        else:
            result.append(card)
    assert [c for c in result if c['year'] != 2018] == preserved
    path.write_text(json.dumps(result, ensure_ascii=False, indent=1) + '\n')
    pages = [f'## Physical page {i}\n\n' + page.get_text(sort=True) for i, page in enumerate(scheme, 1)]
    text = '# SEC LCVP 2018 Common Level written marking scheme\n\n' + '\n\n'.join(pages)
    (ROOT / 'examiner-reports/lcvp/schemes/2018-cl.md').write_text('\n'.join(line.rstrip() for line in text.splitlines()).rstrip() + '\n')
    review['status'] = 'source-authored; independent-sweep-complete; validation-pending'
    review['tasks'] = [dict(id=c['id'], questionRef=c['questionRef'], marks=c['totalMarks'], topicId=c['topicId']) for c in cards]
    REVIEW.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    cards, scheme = build()
    if '--write' in sys.argv:
        write(cards, scheme)
    else:
        print(json.dumps(cards, ensure_ascii=False, indent=2))
