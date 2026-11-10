#!/usr/bin/env python3
"""Original-PDF selectors following the independent 58-page 2024 census.

This module replaces only this sitting. Its 39 existing identities, including
C7aii for the complete activity/role profile, are retained.
"""
import hashlib
import json
import re
import sys
import fitz
from lcvp_review_2026 import ROOT, tidy, select, numbered, point, criterion, menu, partial
from lcvp_review_2025 import paired_rows

REVIEW = ROOT / 'scripts/markbank/authoring/lcvp/2024-cl-main-review.json'
PAPER = 'paper-trail-corpus/exampapers/2024/LC462CLP000EV.pdf'
SCHEME = 'paper-trail-corpus/markingschemes/2024/LC462CLP000EV.pdf'
HASHES = {PAPER: '59764baea4b1a88cfbe2be04276a3be6b21ff324ae113ec6da6bf1c4e9fecf74',
          SCHEME: '62fa33261a67ea4c80cea654d4e33d49380281db4d34d002013ae9139c7cb7d4'}
VIDEO_URL = 'https://www.examinations.ie/archive/exampapers/2024/LC462CLP031EV.mov'
ADDED_IDS = {'lcvp-2024-cl-' + s for s in ['b3iii', 'c1bi', 'c1bii', 'c1ci', 'c2a', 'c6a']}


def documents():
    for path, expected in HASHES.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
    return fitz.open(ROOT / PAPER), fitz.open(ROOT / SCHEME)


def page_raw(doc, number):
    page = doc[number - 1]
    cut = page.rect.height - 15
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            value = tidy(''.join(span['text'] for span in line['spans']))
            if line['bbox'][1] > page.rect.height * .82 and (
                re.fullmatch(r'\d{1,2}', value)
                or value.startswith('Leaving Certificate Vocational Programme')
                or value == 'Link Modules Examination'
            ):
                cut = min(cut, line['bbox'][1] - 2)
    return page.get_text(clip=fitz.Rect(0, 15, page.rect.width, cut), sort=True)


def split_raw(value, pattern, expected):
    """Keep line boundaries until the printed task labels have been separated."""
    matches = list(re.finditer(pattern, value, re.M))
    assert [m[1] for m in matches] == expected, (expected, [m[1] for m in matches], value[:160])
    return {m[1]: value[m.end():matches[i + 1].start() if i + 1 < len(matches) else len(value)]
            for i, m in enumerate(matches)}


def scheme_parts(doc):
    sections = split_raw('\n'.join(page_raw(doc, n) for n in range(2, 17)),
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
                    if (q, letter) in [('1', 'b'), ('1', 'c'), ('4', 'd')]:
                        prefix = part.split('(i)', 1)[0]
                        for roman, sub in split_raw(part, r'^\s*\((i{1,2})\)\s*', ['i', 'ii']).items():
                            # C1(c)'s first two-mark allocation is printed in its parent introduction.
                            if q == '1' and letter == 'c' and roman == 'i':
                                sub = prefix + '\n' + sub
                            out[(section, int(q), letter, roman)] = tidy(sub)
                    else:
                        out[(section, int(q), letter, None)] = tidy(part)
    assert len(out) == 45, len(out)
    return out


PAGES = {('A', q, None, None): p for q, p in enumerate([4, 4, 4, 5, 5, 6, 7, 8], 1)}
PAGES[('B', 1, None, None)] = 10
PAGES.update({('B', q, None, r): 9 + q for q, rs in [(2, ['i', 'ii']), (3, ['i', 'ii', 'iii'])] for r in rs})
PAGES.update({('C', q, l, None): 16 + (q - 1) * 3 + {'a': 0, 'b': 0, 'c': 1, 'd': 2}[l]
              for q in range(1, 8) for l in 'abcd'})
for q, letter in [(1, 'b'), (1, 'c'), (4, 'd')]:
    page = PAGES.pop(('C', q, letter, None))
    PAGES.update({('C', q, letter, r): page for r in ['i', 'ii']})


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
        attribution='SEC LCVP Link Modules 2024 Common Level — © State Examinations Commission.',
        presentationNote='Read the complete original source and question in context.')


def table_cells(doc, number):
    """Original ruled-grid selection; geometry is asserted in the source gate."""
    page = doc[number - 1]
    expected_rows, expected_columns = {5: (2, 2), 9: (6, 3), 10: (9, 2), 12: (6, 3)}[number]
    rules = [item[1] for path in page.get_drawings() for item in path['items']
             if item[0] == 're' and item[1].width < 1 and item[1].height > 5]
    xs = sorted({round(rect.x0, 2) for rect in rules})
    assert len(xs) == expected_columns + 1, (number, xs)
    ys = sorted({(round(rect.y0, 2), round(rect.y1, 2)) for rect in rules if abs(rect.x0 - xs[0]) < .1})
    assert len(ys) == expected_rows, (number, ys)
    for x in xs:
        assert sorted({(round(r.y0, 2), round(r.y1, 2)) for r in rules if abs(r.x0 - x) < .1}) == ys
    result = []
    for upper, lower in ys:
        row = []
        for left, right in zip(xs, xs[1:]):
            clip = fitz.Rect(left, upper, right, lower)
            lines = []
            # One source span crosses two cells on physical page 9; select
            # original glyph centres rather than assigning the whole span.
            for block in page.get_text('rawdict')['blocks']:
                for line in block.get('lines', []):
                    chars = [char for span in line['spans'] for char in span['chars']
                             if clip.contains(fitz.Point((char['bbox'][0] + char['bbox'][2]) / 2,
                                                         (char['bbox'][1] + char['bbox'][3]) / 2))]
                    if chars:
                        lines.append((line['bbox'][1], line['bbox'][0], ''.join(char['c'] for char in chars)))
            row.append(tidy(' '.join(value for _, _, value in sorted(lines))))
        result.append(row)
    assert sum(not value for row in result for value in row) == (1 if number in [9, 10] else 0), (number, result)
    return result


def business_options(scheme):
    cells = table_cells(scheme, 5)
    assert len(cells) == 2 and all(len(row) == 2 for row in cells)
    return [tidy(cells[0][i] + ' ' + cells[1][i]) for i in range(2)]


def build():
    paper, scheme = documents()
    blocks = scheme_parts(scheme)
    rows, totals, topics = {}, {}, {}
    def put(key, mark, topic, value):
        rows[key], totals[key], topics[key] = value, mark, topic
    def a(n): return ('A', n, None, None)
    def b(n, r=None): return ('B', n, None, r)
    def c(n, l, r=None): return ('C', n, l, r)
    put(a(1), 1, '1-2', [point('title', select(blocks[a(1)], '1 mark'), 1)])
    for n, count, expected, topic in [(2, 2, 4, '1-2'), (3, 3, 4, '1-2'), (4, 2, 5, '0-4')]:
        put(a(n), count, topic, menu(blocks[a(n)], count, 1, expected))
    put(a(5), 4, '0-4', partial(blocks[a(5)], 2, 2, 4))
    for n, expected, topic in [(6, 7, '1-2'), (7, 4, '0-1')]:
        put(a(n), 6, topic, menu(blocks[a(n)], 3, 2, expected))
        rows[a(n)][0]['contextNote'] += ' Original allocation is 3 @ 2m (0/2), expansion needed. Each complete expanded response receives 2 or 0; there is no 1-mark step.'
    put(a(8), 6, '0-1', partial(blocks[a(8)], 3, 2, 6))
    for key, count, expected, topic in [(b(1), 3, 10, '1-0'), (b(2, 'i'), 3, 5, '1-1'),
        (b(2, 'ii'), 2, 3, '1-1'), (b(3, 'i'), 2, 7, '1-1'), (b(3, 'ii'), 3, 9, '1-0')]:
        put(key, count * 2, topic, partial(blocks[key], count, 2, expected))
    option_models = []
    for cell, expected in zip(business_options(scheme), [6, 8]):
        values = [tidy(v) for v in cell.split('•')]
        assert len(values) == expected + 1, values
        option_models.append(values)
    put(b(3, 'iii'), 4, '1-1', [criterion('option', 'Option', 1, [0, 1],
        'Choose ONE of the two complete printed options, 1 mark. All THREE reasons must support that SAME option. '
        + ' | '.join(v[0] for v in option_models)), criterion('reasons', '3 valid reasons', 3, [0, 1],
        'Three distinct matching reasons, 1 mark each. Both full source pools are preserved: '
        + ' | '.join(v[0] + ': ' + ' / '.join(v[1:]) for v in option_models))])

    specs = [(1, 'a', None, 2, 2, 11, '1-0'), (1, 'c', 'ii', 2, 2, 6, '1-1'),
        (1, 'd', None, 3, 3, 13, '1-1'), (2, 'c', None, 3, 2, 10, '1-1'),
        (3, 'c', None, 3, 2, 7, '1-4'), (4, 'a', None, 2, 2, 7, '0-1'),
        (4, 'b', None, 3, 2, 7, '0-3'), (5, 'b', None, 3, 2, 12, '0-2'),
        (5, 'd', None, 3, 3, 5, '0-2'), (6, 'b', None, 3, 2, 7, '0-0'),
        (6, 'c', None, 3, 2, 6, '0-0'), (6, 'd', None, 3, 3, 10, '0-0'),
        (7, 'b', None, 3, 2, 8, '0-0'), (7, 'c', None, 3, 2, 11, '0-0'),
        (7, 'd', None, 3, 3, 14, '0-0')]
    for q, letter, roman, count, per, expected, topic in specs:
        key = c(q, letter, roman)
        put(key, count * per, topic, partial(blocks[key], count, per, expected))
    rows[c(1, 'd')][0]['contextNote'] += ' Each profile is a reason plus TWO valid expansions; no repetition of expansions.'
    rows[c(6, 'd')][0]['contextNote'] += ' No repetition of points.'
    key = c(1, 'b', 'i')
    put(key, 4, '1-1', [point('research-type', select(blocks[key], 'Type of Research =', '(1m)'), 1,
        'Required type of research, 1 mark; explanation is a separate required three-mark component.'),
        criterion('explanation', select(blocks[key], 'Desk Research is', 'Forecast Growth', include=True), 3, [0, 1],
        'Explanation 3@1m. Credit three valid content points in the complete source definition; no additional mandatory phrase set is inferred.')])
    key = c(1, 'b', 'ii')
    conclusion = select(blocks[key], 'Any relevant conclusion', include=True)
    put(key, 2, '1-1', [criterion('conclusion', conclusion, 1, [0, 1, 2],
        'ONE relevant conclusion, 2 marks (1+1). It MUST refer to the table years or percentages. All four original examples remain visible.')])
    key = c(1, 'c', 'i')
    put(key, 2, '1-1', [criterion('definition', select(blocks[key], 'Any communication strategy', include=True), 1, [0, 1, 2],
        'Complete original definition; 2 marks (1+1). No extra internal quota is inferred.')])
    key = c(2, 'a')
    put(key, 4, '1-1', [criterion('business', 'Name of any business', 1, [0, 2],
        'Name the business YOU invited, 2 or 0. The reason must refer to this same business; no personal model is invented.'),
        criterion('reason', 'Any valid reason', 1, [0, 2],
        'Explain why YOU chose to invite that SAME business, 2 or 0. No internal 1-mark step is printed.')])
    key = c(2, 'b')
    agenda = numbered(blocks[key], 8)
    put(key, 6, '1-1', [point('heading', 'AGENDA', 1, 'Required heading AGENDA, 1 mark.'),
        point('officers', agenda[0], 1, 'COMPULSORY agenda item: election of officers, 1 mark. Four other distinct valid agenda items earn 1 each.'),
        dict(id='other-items', kind='anyN', verbatim='Other agenda items', marks=4, openList=True,
            group=dict(claimMax=4, perOption=1, options=agenda[1:]),
            contextNote='Choose FOUR other items across the complete seven-item pool. These cannot replace the required heading or election of officers.')])
    key = c(2, 'd')
    put(key, 9, '1-1', paired_rows(3, ['Method', 'Expansion', 'Reason method chosen'], [1, 1, 1],
        'THREE matching method + expansion + reason profiles. No repetition of reason allowed. Full original guidance: '
        + ' | '.join(numbered(blocks[key], 7))))
    for key, pn, expected, topic in [(c(3, 'a'), 9, 17, '1-4'), (c(5, 'a'), 12, 18, '0-2')]:
        cells = [v for row in table_cells(scheme, pn) for v in row if v]
        assert len(cells) == expected
        put(key, 4, topic, [dict(id='responses', kind='anyN', verbatim=tidy(blocks[key].split('4 marks', 1)[0]),
            marks=4, openList=True, group=dict(claimMax=4, perOption=1, options=cells),
            contextNote=f'FOUR distinct responses at 1 mark each. All {expected} original table cells are preserved as separate options.')])
    key = c(3, 'b')
    put(key, 6, '1-4', [criterion('questions', 'Three questions', 3, [0, 2],
        'Three suitable questions about ONE aspect chosen in C3(a), 2 or 0 each. No repetition; each question must be specific to that same aspect. Original guidance: '
        + select(blocks[key], 'Three questions relevant', include=True)
        + '. The source supplies a grid, not completed model questions; no models are invented.')])
    key = c(3, 'd')
    issues = table_cells(scheme, 10)
    put(key, 9, '1-4', paired_rows(3, ['Challenge/Issue', 'First way to overcome', 'Second way to overcome'], [1, 1, 1],
        'THREE different issue profiles: issue 1 mark + TWO matching ways to overcome, 1 mark each. '
        'Each source row is kept paired. Some printed examples contain only one illustrative way; no second model is invented. Full table: '
        + ' | '.join(' → '.join(value for value in row if value) for row in issues)))
    put(c(4, 'c'), 6, '0-3', menu(blocks[c(4, 'c')], 6, 1, 11))
    put(c(4, 'd', 'i'), 3, '0-3', menu(blocks[c(4, 'd', 'i')], 3, 1, 7))
    key = c(4, 'd', 'ii')
    diary = numbered(blocks[key], 4)
    put(key, 6, '0-3', [criterion('career', diary[0], 1, [0, 1, 2],
        'COMPULSORY career aspirations/future studies response, 2 marks (1+1). Explain YOUR evaluation; no completed personal model is invented.'),
        criterion('other-applications', diary[1].split(' at ', 1)[0], 2, [0, 1, 2],
        'TWO other applications, each 2 marks (1+1). These cannot replace the compulsory career/future studies point. Full original guidance: '
        + ' | '.join(diary[1:]))])
    key = c(5, 'c')
    put(key, 6, '1-3', paired_rows(3, ['Resource', 'Why needed'], [1, 1],
        'THREE matched resource/reason profiles, 1+1 each. The reason MUST relate to this Apprenticeship Fair. Full original guidance: '
        + ' | '.join(numbered(blocks[key], 6))))
    key = c(6, 'a')
    definition = select(blocks[key], 'An inclusive workplace', 'Mix of people', include=True)
    expansions = select(blocks[key], 'Not discriminated', include=True)
    put(key, 4, '0-0', [point('mix', 'Mix of people', 1, 'Required opening component, 1 mark. Original definition: ' + definition),
        criterion('expansions', '3 expansions', 3, [0, 1],
        'THREE expansion points, 1 mark each, in addition to the required mix of people. Complete original guidance: ' + expansions)])
    key = c(7, 'a')
    put(key, 4, '1-3', [criterion('activity', 'Name of the activity', 1, [0, 2],
        'Name ONE LCVP team activity YOU participated in, 2 or 0. Keep the matching role within the same task.'),
        criterion('role', 'Brief explanation of the role', 1, [0, 2],
        'Briefly explain YOUR role in that SAME activity, 2 or 0. No completed personal activity/role model is printed or invented.')])
    assert set(rows) == set(blocks) == set(PAGES), (set(blocks) - set(rows), set(rows) - set(blocks))

    case = select(tidy(page_raw(paper, 9)), 'Section B Case Study 30 marks')
    stems = {n: tidy(re.sub(r'^Q\.\s*\d+\s+25\s+marks\s*', '',
        page_raw(paper, 16 + (n - 1) * 3).split('(a)', 1)[0])) for n in range(1, 8)}
    cards = []
    for key in blocks:
        section, q, letter, roman = key
        suffix = section.lower() + str(q) + (letter or '') + (roman or '')
        if key == c(7, 'a'):
            suffix = 'c7aii'  # Stable old identity now contains the complete original profile.
        ref = f'2024 CL Section {section} Q{q}' + (f'({letter})' if letter else '') + (f'({roman})' if roman else '')
        card = dict(id='lcvp-2024-cl-' + suffix, subjectId='lcvp', topicId='lcvp-link-modules-' + topics[key],
            conceptId=suffix, level='common', year=2024, section=section, questionRef=ref,
            questionText=question(paper, key), stem=stems[q] if section == 'C' else case if section == 'B' else '',
            figureKey='', labelKey=[], totalMarks=totals[key], rows=rows[key],
            tariffModel=dict(kind='fixed', notation='Original 2024 allocation; complete source guidance retained'),
            sourceMaterial=source([PAGES[key]]))
        if section == 'A':
            card['videoMaterial'] = dict(kind='source-video', label='OFFICIAL VIDEO', title='2024 LCVP audiovisual examination',
                playbackUrl=VIDEO_URL, canonicalUrl=VIDEO_URL, secFileid='LC462CLP031EV.mov',
                attribution='State Examinations Commission — original 2024 Common Level English audiovisual recording.',
                presentationNote='Watch the original Recruitment of Volunteers sequence with its sound before answering. Follow the original printed viewing instructions. Use the original source link if embedded playback is unavailable.')
            card['additionalSourceMaterials'] = [source([3], title='Original audiovisual instructions')]
        elif section == 'B':
            card['sourceMaterial'] = source([9], 'source-text', 'So Soft by Sandra — complete case study')
            card['additionalSourceMaterials'] = [source([PAGES[key]])]
        elif section == 'C' and q == 1 and letter == 'b':
            card['sourceMaterial'] = source([16], title='Original growth table, attribution and question')
            parent = re.split(r'^\s*\(b\)\s*', page_raw(paper, 16), maxsplit=1, flags=re.M)[1].split('(i)', 1)[0]
            card['stem'] += ' ' + tidy(re.sub(r'\(\d+\s+marks?\)', '', parent))
        elif section == 'C' and q == 1 and letter == 'c':
            parent = re.split(r'^\s*\(c\)\s*', page_raw(paper, 17), maxsplit=1, flags=re.M)[1].split('(i)', 1)[0]
            card['stem'] += ' ' + tidy(parent)
        elif key == c(3, 'b'):
            card['stem'] += ' ' + question(paper, c(3, 'a'))
        cards.append(card)
    assert len(cards) == 45 and sum(card['totalMarks'] for card in cards) == 235
    return cards, scheme


def write(cards, scheme):
    path = ROOT / 'scripts/markbank/authored/lcvp.json'
    old = json.loads(path.read_text())
    prior = [c for c in old if c['year'] == 2024]
    preserved = [c for c in old if c['year'] != 2024]
    assert len(preserved) == 322 and len(prior) in [39, 45]
    assert {c['id'] for c in prior} <= {c['id'] for c in cards}
    assert {c['id'] for c in cards} - {c['id'] for c in prior} in [set(), ADDED_IDS]
    result, inserted = [], False
    for card in old:
        if card['year'] == 2024:
            if not inserted:
                result.extend(cards)
                inserted = True
        else:
            result.append(card)
    assert [c for c in result if c['year'] != 2024] == preserved
    path.write_text(json.dumps(result, ensure_ascii=False, indent=1) + '\n')
    transcript = '# SEC LCVP 2024 Common Level written marking scheme\n\n'
    pages = []
    for i, page in enumerate(scheme, 1):
        value = f'## Physical page {i}\n\n' + page.get_text(sort=True)
        if i in [5, 9, 10, 12]:
            # Preserve the raw page above and also its literal ruled-cell order.
            # Raw sorted text interleaves columns inside wrapped phrases such as
            # Principal economic activities. These are PDF-selected characters,
            # not typed replacements or an exemption from source matching.
            value += '\n\n### Original ruled table — character-centre cell order\n\n'
            value += '\n'.join(' | '.join(row).rstrip() for row in table_cells(scheme, i))
        pages.append(value)
    transcript += '\n\n'.join(pages)
    (ROOT / 'examiner-reports/lcvp/schemes/2024-cl.md').write_text(transcript.rstrip() + '\n')
    review = json.loads(REVIEW.read_text())
    review['status'] = 'source-authored; independent-sweep-complete; validation-pending'
    review['tasks'] = [dict(id=c['id'], questionRef=c['questionRef'], marks=c['totalMarks'], topicId=c['topicId']) for c in cards]
    review['legacyCorrections'] = dict(retainedStableIds=39, addedIds=sorted(ADDED_IDS),
        preservedExpandedIdentity='lcvp-2024-cl-c7aii now contains whole C7(a) activity name plus matching role, four marks; both old ID and concept are retained.')
    review['heldNumericScoring'] = []
    REVIEW.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    cards, scheme = build()
    if '--write' in sys.argv:
        write(cards, scheme)
    else:
        print(json.dumps(cards, ensure_ascii=False, indent=2))
