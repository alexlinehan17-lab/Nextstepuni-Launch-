#!/usr/bin/env python3
"""Original-source selectors after the independent 65-page 2022 main sweep."""
import hashlib
import json
import re
import sys
import fitz
from lcvp_review_2026 import ROOT, tidy, select, numbered, point, criterion, menu, partial
from lcvp_review_2025 import paired_rows
from lcvp_review_2024 import split_raw

REVIEW = ROOT / 'scripts/markbank/authoring/lcvp/2022-cl-main-review.json'
PAPER = 'paper-trail-corpus/exampapers/2022/LC462CLP000EV.pdf'
SCHEME = 'paper-trail-corpus/markingschemes/2022/LC462CLP000EV.pdf'
HASHES = {PAPER: 'aed2d4bfd2d92123bb891bf3d139f0e256472209385b5884811ab1e1ef729600',
          SCHEME: '34482210d864fc13e7d0c4b86a058a03108545a067ace49b82973a4db84b9338'}
ADDED_IDS = {'lcvp-2022-cl-' + key for key in ['b2i', 'c1c', 'c2a', 'c2b', 'c2d', 'c5b', 'c6c']}
VIDEO_URL = 'https://www.examinations.ie/archive/exampapers/2022/LC462CLP031EV.mov'


def documents():
    for path, expected in HASHES.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
    return fitz.open(ROOT / PAPER), fitz.open(ROOT / SCHEME)



def page_raw(doc, number):
    page = doc[number - 1]
    cut = page.rect.height - 15
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            value = tidy(''.join(span['text'] for span in line['spans']))
            box = fitz.Rect(line['bbox'])
            centre = (box.x0 + box.x1) / 2
            # A standalone 3 in a right-hand 3 x 1m tariff is NOT a footer.
            # The actual numeric footer is centred below 90% of the page.
            numeric_footer = (re.fullmatch(r'\d{1,2}', value)
                              and box.y0 > page.rect.height * .9
                              and .4 * page.rect.width < centre < .6 * page.rect.width)
            named_footer = box.y0 > page.rect.height * .82 and (
                value.startswith('Leaving Certificate Vocational Programme')
                or value == 'Link Modules Examination')
            if numeric_footer or named_footer:
                cut = min(cut, box.y0 - 2)
    return page.get_text(clip=fitz.Rect(0, 15, page.rect.width, cut), sort=True)


def scheme_parts(doc, raw=False):
    sections = split_raw('\n'.join(page_raw(doc, n) for n in range(4, 22)),
                         r'^\s*Section ([ABC])\s+', list('ABC'))
    out = {}
    for section, value in sections.items():
        questions = split_raw(value, r'^\s*Q\.\s*(\d+)\s*',
                              [str(n) for n in range(1, {'A': 8, 'B': 3, 'C': 7}[section] + 1)])
        for q, block in questions.items():
            if section == 'A' or (section == 'B' and q == '1'):
                out[(section, int(q), None, None)] = block if raw else tidy(block)
            elif section == 'B':
                for roman, part in split_raw(block, r'^\s*\((i{1,3})\)\s*',
                                             ['i', 'ii', 'iii']).items():
                    out[(section, int(q), None, roman)] = part if raw else tidy(part)
            else:
                for letter, part in split_raw(block, r'^\s*\(([abcd])\)\s*', list('abcd')).items():
                    if (q, letter) in [('6', 'a'), ('7', 'd')]:
                        for roman, sub in split_raw(part, r'^\s*\((i{1,2})\)\s*', ['i', 'ii']).items():
                            out[(section, int(q), letter, roman)] = sub if raw else tidy(sub)
                    else:
                        out[(section, int(q), letter, None)] = part if raw else tidy(part)
    assert len(out) == 45, len(out)
    return out


PAGES = {('A', q, None, None): p for q, p in enumerate([4, 4, 4, 5, 5, 6, 7, 8], 1)}
PAGES[('B', 1, None, None)] = 11
PAGES.update({('B', q, None, r): 10 + q for q, rs in [(2, ['i', 'ii', 'iii']), (3, ['i', 'ii', 'iii'])] for r in rs})
PAGES.update({('C', q, l, None): 18 + (q - 1) * 3 + {'a': 0, 'b': 0, 'c': 1, 'd': 2}[l]
              for q in range(1, 8) for l in 'abcd'})
for q, letter in [(6, 'a'), (7, 'd')]:
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
        attribution='SEC LCVP Link Modules 2022 Common Level — © State Examinations Commission.',
        presentationNote='Read the complete original source and question in context.')


def lines_between(value, start, end=None, expected=None):
    assert value.count(start) == 1, start
    value = start + value.split(start, 1)[1]
    if end:
        assert end in value
        value = value.split(end, 1)[0]
    lines = [tidy(line) for line in value.splitlines() if tidy(line)]
    if expected is not None:
        assert len(lines) == expected, (expected, lines)
    return lines


def explicit_menu(label, options, count, note=''):
    return [dict(id='responses', kind='anyN', verbatim=label, marks=count,
        openList=True, group=dict(claimMax=count, perOption=1, options=options), contextNote=note)]



def line_numbered(value, expected):
    matches = list(re.finditer(r'^\s*(\d+)\.\s+', value, re.M))
    assert [int(m[1]) for m in matches] == list(range(1, expected + 1)), (expected, value)
    return [tidy(value[m.end():matches[i + 1].start() if i + 1 < len(matches) else len(value)])
            for i, m in enumerate(matches)]


def csr_pools(raw):
    names = ['Community', 'Workplace', 'Environment', 'Marketplace']
    pools = {}
    for i, (name, count) in enumerate(zip(names, [7, 7, 6, 8])):
        lines = lines_between(raw, '\n' + name + '\n', '\n' + names[i + 1] + '\n' if i < 3 else None)
        assert lines.pop(0) == name and len(lines) == count, lines
        pools[name] = lines
    return pools


def comparison_cells(doc):
    page = doc[17]
    rules = [item[1] for path in page.get_drawings() for item in path['items']
             if item[0] == 're' and item[1].width < 1 and item[1].height > 5]
    xs = sorted({round(rect.x0, 2) for rect in rules})
    ys = sorted({(round(rect.y0, 2), round(rect.y1, 2)) for rect in rules if abs(rect.x0 - xs[0]) < .1})
    assert len(xs) == 3 and len(ys) == 7, (xs, ys)
    for x in xs:
        assert sorted({(round(r.y0, 2), round(r.y1, 2)) for r in rules if abs(r.x0 - x) < .1}) == ys
    rows = []
    for upper, lower in ys:
        row = []
        for left, right in zip(xs, xs[1:]):
            clip = fitz.Rect(left, upper, right, lower)
            row.append(char_text(page, clip))
        rows.append(row)
    assert all(v for row in rows for v in row)
    return rows


def char_text(page, clip, excluded=None):
    lines = []
    for block in page.get_text('rawdict')['blocks']:
        for line in block.get('lines', []):
            chars = []
            for span in line['spans']:
                for char in span['chars']:
                    centre = fitz.Point((char['bbox'][0] + char['bbox'][2]) / 2,
                                        (char['bbox'][1] + char['bbox'][3]) / 2)
                    if clip.contains(centre) and (excluded is None or not excluded.contains(centre)):
                        chars.append(char['c'])
            if chars:
                lines.append((line['bbox'][1], line['bbox'][0], ''.join(chars)))
    return tidy(' '.join(value for _, _, value in sorted(lines)))


def email_source(doc):
    page = doc[18]
    rectangles = [item[1] for path in page.get_drawings() for item in path['items']
                  if item[0] == 're' and item[1].width > 100 and item[1].height > 100]
    assert len(rectangles) == 2
    box = max(rectangles, key=lambda r: r.width * r.height)
    summary = char_text(page, box)
    labels = re.findall(r'(.+?)\s+1m', select(summary, 'Summary of marks', 'Total'))
    labels = [tidy(v) for v in labels]
    assert len(labels) == 8 and summary.endswith('Total 8m'), summary
    named = {}
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            value = tidy(''.join(span['text'] for span in line['spans']))
            if value.startswith('To: paul_') or value == 'Rebecca O’Sullivan':
                named[value] = fitz.Rect(line['bbox'])
    assert len(named) == 2, named
    upper = min(r.y0 for r in named.values()) - 1
    lower = max(r.y1 for r in named.values()) + 1
    model = char_text(page, fitz.Rect(0, upper, page.rect.width, lower), excluded=box)
    assert model.startswith('To: paul_d@svp.ie') and model.endswith('Rebecca O’Sullivan')
    assert 'Summary of marks' not in model and '2-3 hours per week' in model
    return model, labels, summary


def build():
    paper, scheme = documents()
    blocks, raw = scheme_parts(scheme), scheme_parts(scheme, raw=True)
    rows, totals, topics = {}, {}, {}
    def put(key, mark, topic, value):
        rows[key], totals[key], topics[key] = value, mark, topic
    def a(n): return ('A', n, None, None)
    def b(n, r=None): return ('B', n, None, r)
    def c(n, l, r=None): return ('C', n, l, r)
    put(a(1), 1, '1-0', explicit_menu('one benefit', lines_between(raw[a(1)], 'Not doing', '1 mark', 4), 1))
    put(a(2), 2, '0-0', explicit_menu('Two tourism jobs', lines_between(raw[a(2)], 'Hotel', expected=5), 2))
    for n, count, expected in [(3, 3, 4), (4, 2, 8), (5, 4, 7)]:
        put(a(n), count, '1-1', menu(blocks[a(n)], count, 1, expected))
    pools = csr_pools(raw[a(6)])
    put(a(6), 6, '1-1', [criterion('chosen-area', 'Give reasons for your answer.', 6, [0, 1],
        'Choose ONE of the FOUR printed areas and support that SAME area with six distinct content points, 1 mark each. '
        'No separate mark for naming the area is printed. Do not mix reasons from different choices. Complete original pools: '
        + ' | '.join(name + ': ' + ' / '.join(values) for name, values in pools.items()))])
    put(a(7), 6, '1-1', partial(blocks[a(7)], 3, 2, 4,
        'Retain the printed agree/disagree question. No separate agreement mark or invented dissent model is added.'))
    put(a(8), 6, '1-1', partial(blocks[a(8)], 3, 2, 6,
        'Retain the printed agree/disagree question. No separate agreement mark or invented dissent model is added.'))
    put(b(1), 6, '1-0', partial(blocks[b(1)], 3, 2, 8))
    put(b(2, 'i'), 2, '1-1', [point('reward', select(blocks[b(2, 'i')], 'Reward - 1m', 'Risk - 1m'), 1,
        'ONE reward, 1 mark; keep all three source examples. A risk cannot replace the required reward.'),
        point('risk', select(blocks[b(2, 'i')], 'Risk - 1m'), 1,
        'ONE risk, 1 mark; all four source examples retained. Both categories are required.')])
    duties = lines_between(raw[b(2, 'ii')], 'Website development', expected=4)
    put(b(2, 'ii'), 3, '0-1', explicit_menu('3 Duties', duties, 3,
        'THREE duties for the ONE new staff member, 1 mark each; the complete source examples are retained.'))
    put(b(2, 'iii'), 4, '0-1', [point(f'category-{i}', value, 1,
        'All FOUR person-specification categories are required, 1 mark each. Apply them to the SAME new staff member/job from B2(ii); source examples are illustrative.' if i == 1 else '')
        for i, value in enumerate(numbered(blocks[b(2, 'iii')], 4), 1)])
    put(b(3, 'i'), 2, '1-1', [criterion('purpose', select(blocks[b(3, 'i')], '2 x 1m'), 2, [0, 1],
        'Two valid content points, 1 mark each. Preserve the full original explanation without adding category-name quotas.')])
    put(b(3, 'ii'), 6, '1-1', partial(blocks[b(3, 'ii')], 3, 2, 11))
    put(b(3, 'iii'), 2, '1-1', menu(blocks[b(3, 'iii')], 2, 1, 8))
    put(c(1, 'a'), 4, '1-3', menu(blocks[c(1, 'a')], 4, 1, 10))
    rows[c(1, 'a')][0]['contextNote'] += ' No compulsory election-of-officers item or separate Agenda-heading mark is printed for THIS sitting.'
    specs = [(1, 'b', 2, 2, 6, '1-3'), (1, 'd', 3, 3, 4, '1-3'),
        (2, 'c', 4, 2, 11, '0-2'), (3, 'b', 2, 2, 11, '1-0'), (3, 'c', 4, 2, 9, '1-0'),
        (3, 'd', 3, 3, 8, '1-0'), (4, 'a', 2, 2, 11, '0-0'), (4, 'b', 2, 2, 7, '0-0'),
        (4, 'c', 4, 2, 7, '0-0'), (5, 'c', 4, 2, 6, '1-4'), (6, 'd', 3, 3, 8, '1-2'),
        (7, 'c', 4, 2, 10, '0-1')]
    for q, letter, count, per, expected, topic in specs:
        key = c(q, letter)
        put(key, count * per, topic, partial(blocks[key], count, per, expected))
    schedule = select(blocks[c(1, 'c')], 'Schedule of Time', include=True)
    put(c(1, 'c'), 8, '1-3', [point('day', 'Day of the event', 2,
        'The event-day action is a distinct TWO-mark component; no internal 1-mark step is printed. The full original illustrative schedule is retained below.'),
        criterion('actions', 'actions', 5, [0, 1],
        'FIVE other valid actions, 1 mark each, in addition to the two-mark event-day action. The scheme says Six valid actions overall. Complete original two-page schedule: ' + schedule),
        point('sequence', 'sequence of time', 1, 'Sequence of time, 1 mark. Use a coherent running section for THIS fashion-show activity.')])
    put(c(2, 'a'), 4, '0-2', [point('career', 'One valid career', 1,
        'Name ONE career, 1 mark. All three duties must refer to THAT SAME career; no personal model is invented.'),
        criterion('duties', 'Three relevant duties', 3, [0, 1], 'THREE relevant duties for the career you named, 1 mark each. No source model duties are printed or invented.')])
    experiences = numbered(blocks[c(2, 'b')], 6)
    put(c(2, 'b'), 4, '0-2', [point('experience', 'name the experience', 1,
        'Name ONE out-of-school learning experience, 1 mark. Full original options: ' + ' | '.join(experiences)),
        criterion('description', 'description', 3, [0, 1],
        'THREE valid description points about that SAME experience, 1 mark each. The source gives six possible experiences, not a completed personal description; none is invented.')])
    benefit = line_numbered(raw[c(2, 'd')].split('\nBenefits\n', 1)[1].split('\nChallenges\n', 1)[0], 11)
    challenge = line_numbered(raw[c(2, 'd')].split('\nChallenges\n', 1)[1], 9)
    benefit_row = explicit_menu('Benefits', benefit, 4, 'FOUR benefits, 1 mark each. These cannot replace the required FOUR challenges.')[0]
    challenge_row = explicit_menu('Challenges', challenge, 4, 'FOUR challenges, 1 mark each. These cannot replace the required FOUR benefits.')[0]
    benefit_row['id'], challenge_row['id'] = 'benefits', 'challenges'
    put(c(2, 'd'), 9, '0-0', [benefit_row, challenge_row, criterion('other', 'One other point', 1, [0, 1],
        'ONE additional distinct benefit OR challenge, 1 mark. Do not repeat any of the eight points already claimed.')])
    put(c(3, 'a'), 4, '1-0', [criterion('definition', select(blocks[c(3, 'a')], '(0/2)'), 2, [0, 2],
        'Original allocation is 2 x 2m (0/2). Each of the TWO response units is worth 2 or 0; there is no 1-mark partial step. '
        'The complete definition is preserved without inventing a compulsory phrase split.')])
    health = ' | '.join(numbered(blocks[c(4, 'd')], 11))
    put(c(4, 'd'), 9, '0-0', [criterion(f'benefit-{i}', label, 1, [0, 1, 2, 3],
        'THREE benefit profiles (1+1+1): ONE employee benefit, ONE employer benefit and ONE other. '
        'The source gives one undivided model pool; no per-model category assignment is invented. Complete original models: ' + health if i == 1 else
        'Retain this required category; choose a distinct benefit and keep its matching expansions.')
        for i, label in enumerate(['Employee benefit', 'Employer benefit', 'other benefit point'], 1)])
    for key, count, expected in [(c(5, 'a'), 4, 9), (c(5, 'b'), 2, 11)]:
        values = [tidy(v) for v in blocks[key].split('•')[1:]]
        assert len(values) == expected, values
        if key == c(5, 'a'):
            assert values.pop().lower() == 'etc.'
            put(key, 4, '1-4', explicit_menu('sources of employment', values, 4, 'FOUR valid local sources, 1 mark each; source Etc. retains equivalent alternatives.'))
        else:
            put(key, 4, '1-4', [criterion('activities', 'principal economic activities', 2, [0, 1, 2],
                'TWO activity/explanation profiles, 1+1 each. Complete original eleven-option pool: ' + ' | '.join(values))])
    put(c(5, 'd'), 9, '1-4', paired_rows(3, ['Challenge', 'way to overcome'], [2, 1],
        'THREE coherent challenge/solution profiles. Each challenge is worth TWO content marks (1+1); its matching way to overcome is worth ONE. '
        'Do not reverse these allocations. Full original paired examples and open local alternative: ' + ' | '.join(numbered(blocks[c(5, 'd')], 8))))
    organisations = select(blocks[c(6, 'a', 'i')], 'St. Vincent', include=True).split(', ')
    assert len(organisations) == 4
    put(c(6, 'a', 'i'), 2, '1-2', explicit_menu('Two named voluntary organisations', organisations, 2,
        'TWO organisations serving your area, 1 mark each; full four-name example pool and etc. remain.'))
    put(c(6, 'a', 'ii'), 2, '1-2', menu(blocks[c(6, 'a', 'ii')], 2, 1, 6))
    comparisons = comparison_cells(scheme)
    put(c(6, 'b'), 4, '1-2', paired_rows(2, comparisons[0], [1, 1],
        'TWO valid paired comparisons, 1 mark for each side. Keep each voluntary-organisation statement paired with its matching commercial-business contrast. '
        'Complete original six-pair table: ' + ' | '.join(' → '.join(row) for row in comparisons[1:])))
    model, email_labels, _ = email_source(scheme)
    put(c(6, 'c'), 8, '1-2', [point(f'email-{i}', label, 1,
        'EIGHT required email components, 1 mark each. No extra layout or grammar marks. Complete original model: ' + model if i == 1 else '')
        for i, label in enumerate(email_labels, 1)])
    put(c(7, 'a'), 4, '0-1', menu(blocks[c(7, 'a')], 4, 1, 5))
    put(c(7, 'b'), 4, '0-1', menu(blocks[c(7, 'b')], 4, 1, 8))
    rows[c(7, 'c')][0]['contextNote'] += ' Each response must pair the preparation WAY with its matching WHY, 1+1.'
    put(c(7, 'd', 'i'), 3, '0-1', menu(blocks[c(7, 'd', 'i')], 3, 1, 8))
    put(c(7, 'd', 'ii'), 6, '0-1', partial(blocks[c(7, 'd', 'ii')], 3, 2, 4))
    assert set(rows) == set(blocks) == set(PAGES)
    case = select(tidy(page_raw(paper, 10)), 'Section B Case Study 25 marks')
    stems = {n: tidy(re.sub(r'^Q\.\s*\d+\s+25\s+marks\s*', '',
        page_raw(paper, 18 + (n - 1) * 3).split('(a)', 1)[0])) for n in range(1, 8)}
    cards = []
    for key in blocks:
        section, q, letter, roman = key
        suffix = section.lower() + str(q) + (letter or '') + (roman or '')
        ref = f'2022 CL Section {section} Q{q}' + (f'({letter})' if letter else '') + (f'({roman})' if roman else '')
        card = dict(id='lcvp-2022-cl-' + suffix, subjectId='lcvp', topicId='lcvp-link-modules-' + topics[key],
            conceptId=suffix, level='common', year=2022, section=section, questionRef=ref,
            questionText=question(paper, key), stem=stems[q] if section == 'C' else case if section == 'B' else '',
            figureKey='', labelKey=[], totalMarks=totals[key], rows=rows[key],
            tariffModel=dict(kind='fixed', notation='Original 2022 allocation; complete source guidance retained'),
            sourceMaterial=source([PAGES[key]]))
        if section == 'A':
            card['videoMaterial'] = dict(kind='source-video', label='OFFICIAL VIDEO', title='2022 LCVP audiovisual examination',
                playbackUrl=VIDEO_URL, canonicalUrl=VIDEO_URL, secFileid='LC462CLP031EV.mov',
                attribution='State Examinations Commission — original 2022 Common Level English audiovisual recording.',
                presentationNote='Watch the original Corporate Social Responsibility sequence with its sound before answering. Follow the original printed viewing instructions. Use the original source link if embedded playback is unavailable.')
            card['additionalSourceMaterials'] = [source([3], title='Original audiovisual instructions')]
        elif section == 'B':
            card['sourceMaterial'] = source([10], 'source-text', 'Alex and Rami — complete case study')
            card['additionalSourceMaterials'] = [source([PAGES[key]])]
            if key == b(2, 'iii'):
                card['stem'] += ' ' + question(paper, b(2, 'ii'))
        cards.append(card)
    assert len(cards) == 45 and sum(card['totalMarks'] for card in cards) == 230
    return cards, scheme

def write(cards, scheme):
    path = ROOT / 'scripts/markbank/authored/lcvp.json'
    old = json.loads(path.read_text())
    prior = [c for c in old if c['year'] == 2022]
    preserved = [c for c in old if c['year'] != 2022]
    assert len(preserved) == 331 and len(prior) in [38, 45]
    assert {c['id'] for c in prior} <= {c['id'] for c in cards}
    assert {c['id'] for c in cards} - {c['id'] for c in prior} in [set(), ADDED_IDS]
    result, inserted = [], False
    for card in old:
        if card['year'] == 2022:
            if not inserted:
                result.extend(cards)
                inserted = True
        else:
            result.append(card)
    assert [c for c in result if c['year'] != 2022] == preserved
    path.write_text(json.dumps(result, ensure_ascii=False, indent=1) + '\n')
    transcript = '# SEC LCVP 2022 Common Level written marking scheme\n\n'
    pages = []
    for i, page in enumerate(scheme, 1):
        value = f'## Physical page {i}\n\n' + page.get_text(sort=True)
        if i == 18:
            value += '\n\n### Original ruled table — character-centre cell order\n\n'
            value += '\n'.join(' | '.join(row).rstrip() for row in comparison_cells(scheme))
        if i == 19:
            model, labels, summary = email_source(scheme)
            value += '\n\n### Original email outside its separate mark box\n\n' + model + '\n\n' + summary
        pages.append(value)
    transcript += '\n\n'.join(pages)
    (ROOT / 'examiner-reports/lcvp/schemes/2022-cl.md').write_text(transcript.rstrip() + '\n')
    review = json.loads(REVIEW.read_text())
    review['status'] = 'source-authored; independent-sweep-complete; validation-pending'
    review['tasks'] = [dict(id=c['id'], questionRef=c['questionRef'], marks=c['totalMarks'], topicId=c['topicId']) for c in cards]
    review['legacyCorrections'] = dict(retainedStableIds=38, addedIds=sorted(ADDED_IDS),
        previousPrintedMarks=191, correctedPrintedMarks=230,
        canonicalTopics='Reviewed against curriculumRegistry.ts; old metadata corrected without changing any old ID or concept. Original Atlas assessment-format anchors preserved.')
    review['heldNumericScoring'] = []
    REVIEW.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    cards, scheme = build()
    if '--write' in sys.argv:
        write(cards, scheme)
    else:
        print(json.dumps(cards, ensure_ascii=False, indent=2))
