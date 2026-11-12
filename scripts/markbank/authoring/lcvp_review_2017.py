#!/usr/bin/env python3
"""Original-source selectors after the independent 48-page 2017 review."""
import hashlib
import json
import re
import sys
import fitz
from lcvp_review_2026 import ROOT, tidy, select, point, criterion
from lcvp_review_2024 import split_raw
from lcvp_review_2022 import page_raw
from lcvp_review_2018 import choice_row, response_row, before_rate, models
from lcvp_identity import concept_id

REVIEW = ROOT / 'scripts/markbank/authoring/lcvp/2017-cl-main-review.json'
PAPER = 'paper-trail-corpus/exampapers/2017/LC462CLPO00EV.pdf'
SCHEME = 'paper-trail-corpus/markingschemes/2017/LC462CLP000EV.pdf'
HASHES = {PAPER: '9a37c1d576ef1166a0343814c53d69ba9583d0bd0ac1ffbc22b1a712e56fca71',
          SCHEME: 'ea64635f6bdbebea17ce35fb814768be75a929aea94c0abe9900a86d8aa7d46f'}
VIDEO_URL = 'https://www.examinations.ie/archive/exampapers/2017/LC462CLP031EV.mp4'


def documents():
    for path, expected in HASHES.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
    return fitz.open(ROOT / PAPER), fitz.open(ROOT / SCHEME)


def paper_raw(doc, number):
    """Remove only identified office-use spans and the original page footer."""
    page = doc[number - 1]
    lines = []
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            kept = []
            for span in line['spans']:
                value, box = tidy(span['text']), fitz.Rect(span['bbox'])
                office = value in ['Office Use', 'Only', '1', '2'] and box.x0 > 520 and box.y1 < 110
                footer = re.fullmatch(r'Page \d+ of 32', value) and box.y0 > 800
                if not (office or footer):
                    kept.append(span['text'])
            value = tidy(''.join(kept))
            if value:
                lines.append((line['bbox'][1], line['bbox'][0], value))
    return '\n'.join(value for _, _, value in sorted(lines))


def header_body(raw):
    mark = re.search(r'\b\d+\s+[Mm]arks?\b', raw)
    assert mark, raw[:200]
    return raw[:mark.end()], raw[mark.end():]


def scheme_parts(doc):
    sections = split_raw('\n'.join(page_raw(doc, n) for n in range(4, 15)),
                         r'^\s*Section ([ABC])\s+', list('ABC'))
    out = {}
    for section, value in sections.items():
        questions = split_raw(value, r'^\s*Q\.?\s*(\d+)\s*',
                              [str(n) for n in range(1, {'A': 8, 'B': 3, 'C': 6}[section] + 1)])
        for q, block in questions.items():
            q = int(q)
            if section == 'A' or (section == 'B' and q == 1):
                out[(section, q, None)] = block
            elif section == 'B':
                heading, body = header_body(block)
                for letter, part in split_raw(body, r'^\s*\(([abc])\)\s*', list('abc' if q == 2 else 'ab')).items():
                    out[(section, q, letter)] = heading + '\n' + part
            else:
                for letter, part in split_raw(block, r'^\s*\(([abcd])\)\s*', list('abcd')).items():
                    out[(section, q, letter)] = part
    assert len(out) == 38
    return out


PAGES = {('A', q, None): p for q, p in enumerate([3, 3, 3, 4, 4, 5, 6, 7], 1)}
PAGES[('B', 1, None)] = 9
PAGES.update({('B', q, letter): 8 + q for q in [2, 3] for letter in ('abc' if q == 2 else 'ab')})
PAGES.update({('C', q, letter): 14 + (q - 1) * 3 + {'a': 0, 'b': 0, 'c': 1, 'd': 2}[letter]
              for q in range(1, 7) for letter in 'abcd'})


def question(doc, key):
    section, q, letter = key
    value = paper_raw(doc, PAGES[key])
    if section in ['A', 'B']:
        value = re.split(r'^\s*Q\.\s*' + str(q) + r'\s+', value, maxsplit=1, flags=re.M)[1]
        value = re.split(r'^\s*Q\.\s*\d+\s+', value, maxsplit=1, flags=re.M)[0]
    if letter:
        value = re.split(r'\(' + letter + r'\)\s*', value, maxsplit=1)[1]
        value = re.split(r'\([abcd]\)\s*', value, maxsplit=1)[0]
    value = re.sub(r'\b\d+\s+marks?\b', '', value, flags=re.I)
    return tidy(value)


def contrast_models(scheme):
    """Keep both cells of every original table row, using its printed divider."""
    page = scheme[7]
    dividers = [item[1] for path in page.get_drawings() for item in path['items']
                if item[0] == 're' and item[1].width < 1 and item[1].height > 10
                and 280 < item[1].x0 < 310]
    assert dividers and len({round(r.x0, 2) for r in dividers}) == 1
    split_x = dividers[0].x0
    lines = [(line['bbox'], tidy(''.join(s['text'] for s in line['spans'])))
             for block in page.get_text('dict')['blocks'] for line in block.get('lines', [])]
    starts = [(int(m[1]), box[1]) for box, value in lines
              if (m := re.match(r'^(\d{1,2})\.\s+', value)) and box[0] < split_x and 170 < box[1] < 360]
    assert [n for n, _ in starts] == list(range(1, 11))
    result = []
    for i, (n, top) in enumerate(starts):
        bottom = starts[i + 1][1] if i + 1 < len(starts) else max(r.y1 for r in dividers)
        cells = []
        for left in [True, False]:
            pieces = [(box[1], box[0], value) for box, value in lines
                      if top - .1 <= box[1] < bottom - .1 and bool(box[0] < split_x) == left and value]
            cells.append(tidy(' '.join(v for _, _, v in sorted(pieces))))
        cells[0] = re.sub(r'^' + str(n) + r'\.\s*', '', cells[0])
        assert all(cells), (n, cells)
        result.append(cells[0] + ' — ' + cells[1])
    return result


def component_rows(label, pool, tariffs, guidance):
    """Separate printed component awards, including indivisible two-mark parts."""
    result = []
    for i, tariff in enumerate(tariffs, 1):
        steps = {0}
        for mark in tariff:
            steps = {a + b for a in steps for b in [0, mark]}
        row = criterion(f'response-{i}', label, 1, sorted(steps),
            f'Response {i} of {len(tariffs)}. ' + guidance + ' Complete original guidance: ' + ' | '.join(pool))
        row['parts'] = [dict(id=f'component-{j}', verbatim=f'{mark}m', marks=mark, permittedMarks=[0, mark])
                        for j, mark in enumerate(tariff, 1)]
        result.append(row)
    return result


def source(pages, kind='source-question', title='Original question'):
    return dict(kind=kind, label='OFFICIAL SOURCE', title=title, pages=pages,
                attribution='SEC LCVP Link Modules 2017 Common Level — © State Examinations Commission.',
                presentationNote='Read the complete original source and question in context.')


def build():
    paper, scheme = documents()
    raw = scheme_parts(scheme)
    rows, totals, topics, concepts = {}, {}, {}, {}
    def key(s, q, letter=None): return (s, q, letter)
    def put(k, marks, topic, concept, value):
        rows[k], totals[k], topics[k], concepts[k] = value, marks, topic, concept
    def labelled(k):
        header, body = header_body(raw[k])
        if k[0] == 'B' and k[2]:
            header = split_raw(header, r'^\s*\(([abc])\)\s*', list('abc' if k[1] == 2 else 'ab'))[k[2]]
        return tidy(re.sub(r'\b\d+\s+[Mm]arks?\b', '', header)), body
    def ordinary(k, topic, concept, count, per, expected, rate, binary=False):
        label, body = labelled(k)
        pool = models(before_rate(body, rate), expected)
        if binary or per == 1:
            value = choice_row('responses', label, pool, count, per,
                f'{count} distinct relevant responses; {per} or 0 marks each. All original alternatives remain visible.')
        else:
            value = response_row('responses', label, pool, count, list(range(per + 1)),
                f'Original allocation: {count} responses, each {per} marks in printed 1-mark components. No repeated credit.')
        put(k, count * per, topic, concept, [value])

    a = lambda q: key('A', q)
    b = lambda q, l=None: key('B', q, l)
    c = lambda q, l: key('C', q, l)
    _, body = labelled(a(1))
    pool = [tidy(v) for v in body.splitlines() if v.strip()]
    assert len(pool) == 2
    put(a(1), 1, '1-1', 'computer-games-business', [choice_row('business', 'What type of business', pool, 1, 1)])
    _, body = labelled(a(2))
    put(a(2), 2, '0-3', 'internship-employer', [point('employer', tidy(before_rate(body, r'2m')), 2,
        'The original scheme emphasises Gaming in bold and gives the complete answer 2 marks. No unprinted internal partial tariff is inferred.')])
    label, body = labelled(a(3))
    put(a(3), 3, '0-3', 'employer-work-experience-reasons', [choice_row('reasons', label,
        models(before_rate(body, r'2m\s*\+\s*1m'), 3), 2, 2,
        'Original allocation: 2m + 1m. Credit two distinct reasons from the full three-model pool. The paper why-question is unchanged; the values are response slots, not fixed prices for particular model reasons.', steps=[2, 1])])
    ordinary(a(4), '0-3', 'work-experience-activities', 4, 1, 5, r'4\s*@\s*1m')
    _, body = labelled(a(5))
    before, pool_text = re.split(r'Justification:\s*3\s*@\s*1m', body, maxsplit=1)
    assert tidy(before) == 'YES/NO 1m'
    put(a(5), 4, '0-2', 'realistic-career-path', [point('judgement', 'YES/NO', 1),
        choice_row('justification', 'Justification:', models(pool_text, 5), 3, 1,
            'The source allows YES/NO (1m) plus three justification points (3@1m). Do not force a particular judgement.')])
    ordinary(a(6), '1-1', 'business-challenges', 4, 1, 6, r'4\s*@\s*1\s*m')
    ordinary(a(7), '0-1', 'interview-feedback', 6, 1, 7, r'6\s*@\s*1m')
    ordinary(a(8), '0-3', 'employer-placement-benefits', 6, 1, 6, r'6\s*@\s*1m')

    label, body = labelled(b(1))
    pool = models(before_rate(body, r'Field research'), 8)
    put(b(1), 6, '1-1', 'market-research-methods', [response_row('methods', label, pool, 3, [0, 1, 2],
        'Original 3@2m (1+1); Field research pt 1/2/3/4, Desk research pt 5/6/7/8, Any valid expansion. Three responses from the entire pool; no required field/desk mix.')])
    ordinary(b(2, 'a'), '1-0', 'business-innovation', 2, 1, 5, r'2\s*@\s*1m')
    ordinary(b(2, 'b'), '1-1', 'starting-business-course', 3, 2, 9, r'3\s*@\s*2m\s*\(0/2\)', binary=True)
    ordinary(b(2, 'c'), '1-1', 'business-plan-objectives', 4, 1, 8, r'4\s*@\s*1m')
    label, body = labelled(b(3, 'a'))
    assert 'Contrast must be present' in body and re.search(r'2\s*@\s*1m', body)
    put(b(3, 'a'), 2, '1-0', 'entrepreneur-employee-contrast', [choice_row('contrasts', 'Contrast must be present',
        contrast_models(scheme), 2, 1,
        'Two complete contrasts, 1 mark each. Each paired option reads ENTREPRENEUR — EMPLOYEE in the original table-column order. Both entrepreneur and employee sides must be present in each response; never award separate credit for the two cells. All ten original paired models remain available.')])
    ordinary(b(3, 'b'), '1-1', 'business-success-planning', 5, 2, 9, r'5\s*@\s*2m\s*\(1\+1\)')

    _, body = labelled(c(1, 'a'))
    parts = re.findall(r'(Name the career|Outline of reason career was chosen)\s+2\s+marks', body)
    assert len(parts) == 2
    put(c(1, 'a'), 4, '0-2', 'career-choice-reason', [point(f'component-{i}', v, 2,
        'Name 2 marks and reason 2 marks. The source supplies criteria for the personal response; no model career or unprinted internal 1-mark split is invented.') for i, v in enumerate(parts, 1)])
    _, body = labelled(c(1, 'b'))
    pools = split_raw(body, r'^\s*(Skill|Quality)\s*$', ['Skill', 'Quality'])
    put(c(1, 'b'), 4, '0-2', 'career-skill-quality', [response_row(title.lower(), title,
        [tidy(before_rate(pools[title], r'2m\(1\+1\)'))], 1, [0, 1, 2],
        'ONE skill and ONE quality are required, each 2m(1+1), linked to the same career. Preserve the complete original example pool and its open ellipsis.') for title in pools])
    ordinary(c(1, 'c'), '0-2', 'career-information-sources', 4, 2, 7, r'4\s*@\s*2m\s*\(1\+1\)')
    for k, expected, topic, concept in [(c(1, 'd'), 5, '0-2', 'career-investigation-evaluation'), (c(2, 'c'), 6, '0-0', 'poor-communication-effects')]:
        label, body = labelled(k)
        put(k, 9, topic, concept, component_rows(label, models(before_rate(body, r'3\s*@\s*3m\s*\(1\s*\+\s*2\(0/2\)\)'), expected), [[1, 2]] * 3,
            'THREE distinct responses. Original 3@3m(1+2(0/2)): each has a 1-mark component and a separately controlled binary 0/2 component; no 1-of-2 award.'))
    label, body = labelled(c(2, 'a'))
    put(c(2, 'a'), 2, '0-0', 'effective-communication', [response_row('definition', label,
        [tidy(before_rate(body, r'1m\s*\+\s*1m'))], 2, [0, 1],
        'Original complete answer and 1m + 1m allocation. No fixed semantic division of the definition is invented.')])
    ordinary(c(2, 'b'), '0-0', 'workplace-communication-methods', 3, 2, 5, r'3\s*@\s*2m\s*\(1\s*\+\s*1\)')
    rows[c(2, 'b')][0]['contextNote'] += ' Original instruction: No repetition.'
    label, body = labelled(c(2, 'd'))
    put(c(2, 'd'), 8, '1-0', 'activity-presentation-skills', component_rows(label,
        models(before_rate(body, r'2\s*@\s*3m\(1\+2\)'), 5), [[1, 2], [1, 2], [1, 1]],
        'Original allocation: 2@3m(1+2) and 1@2(1+1). THREE distinct responses use the printed 3,3,2 response slots. The two-mark components have no printed internal one-mark split; do not assign these unequal values to named models.'))
    _, body = labelled(c(3, 'a'))
    assert 'Name of organisation' in body and 'Activity of organisation' in body
    put(c(3, 'a'), 3, '1-2', 'local-voluntary-organisation', [point('name', 'Name of organisation', 1),
        point('activity', 'Activity of organisation', 2, 'Original activity 2m(0/2); no 1-mark step. Use the same named local organisation; no personal model is invented.')])
    ordinary(c(3, 'b'), '1-2', 'volunteering-enquiries', 3, 2, 8, r'3\s*@\s*2m\(0/2\)', binary=True)
    ordinary(c(3, 'c'), '1-2', 'volunteer-responsibilities', 4, 2, 8, r'4\s*@\s*2m\(1\+1\)')
    ordinary(c(3, 'd'), '1-2', 'promoting-volunteering', 4, 2, 6, r'4\s*@\s*2m\(1\+1\)')
    _, body = labelled(c(4, 'a'))
    prefix, remainder = re.split(r'Name\s*[–-]\s*1m', body, maxsplit=1)
    assert not prefix.strip()
    put(c(4, 'a'), 3, '1-1', 'business-visit-objectives', [point('name', 'Name', 1),
        choice_row('objectives', 'two objectives', models(before_rate(remainder, r'2\s*@\s*1m'), 6), 2, 1,
            'Name of the business 1m plus two objectives 1m each, for the same proposed visit.')])
    ordinary(c(4, 'b'), '1-1', 'local-business-benefits', 3, 2, 8, r'3\s*@\s*2m\(1\+1\)')
    _, body = labelled(c(4, 'c'))
    criteria = [tidy(v) for v in re.split(r'1m\s*', body) if tidy(v)]
    assert len(criteria) == 10 and criteria[0] == 'Own address & Business address'
    put(c(4, 'c'), 10, '1-1', 'business-visit-request-letter', [dict(id='letter', kind='criterion',
        verbatim=question(paper, c(4, 'c')), marks=10, permittedMarks=list(range(11)),
        parts=[dict(id=f'criterion-{i}', verbatim=v, marks=1, permittedMarks=[0, 1]) for i, v in enumerate(criteria, 1)],
        contextNote='One complete request letter. Retain all ten original one-mark criteria; Own address & Business address together receive ONE mark. Layout/neatness, spelling and grammar/paragraphs/punctuation each remain separate. No model letter is invented.')])
    ordinary(c(4, 'd'), '1-0', 'teamwork-benefits', 3, 2, 8, r'3\s*@\s*2m\(1\+1\)')
    label, body = labelled(c(5, 'a'))
    put(c(5, 'a'), 4, '0-0', 'responsible-work-ethic', [response_row('definition', label,
        [tidy(before_rate(body, r'2m\s*\+\s*2m'))], 2, [0, 2],
        'Original combined definition and 2m + 2m allocation. Two complete credited components; no fixed descriptor pairing or unprinted 1-mark step.')])
    ordinary(c(5, 'b'), '0-0', 'employer-work-ethic-benefits', 6, 1, 8, r'6\s*@\s*1m')
    ordinary(c(5, 'c'), '0-0', 'employment-contract-content', 6, 1, 9, r'6\s*@\s*1m')
    label, body = labelled(c(5, 'd'))
    put(c(5, 'd'), 9, '0-1', 'recruitment-factors', component_rows(label,
        models(before_rate(body, r'3\s*@\s*3m\s*\(1\s*\+\s*2\)'), 6), [[1, 2]] * 3,
        'THREE distinct factors, original 3@3m(1+2). Keep the separate 1-mark and 2-mark components; no unprinted subdivision of the latter.'))
    ordinary(c(6, 'a'), '0-2', 'career-exhibition-purpose', 2, 1, 5, r'2\s*@\s*1m\s*each')
    label, body = labelled(c(6, 'b'))
    # The guidance sits alongside the numbered headings; remove that exact
    # instruction before extracting the seven headings, then retain it visibly.
    pool_text = re.sub(r'any two valid points under three headings[ \t]*|no marks for headings\.[ \t]*', '', before_rate(body, r'3\s*@\s*2m\(1\+1\)'))
    headings = models(pool_text, 7)
    put(c(6, 'b'), 6, '1-3', 'career-exhibition-plan', [response_row(f'heading-{i}', label, headings, 2, [0, 1],
        f'Heading {i} of THREE open headings: any two valid points under this heading, no marks for headings. Original 3@2m(1+1). All seven model headings remain examples; no closed choose-three list or invented plan points.') for i in range(1, 4)])
    ordinary(c(6, 'c'), '1-3', 'career-exhibition-challenges', 4, 2, 7, r'4\s*@\s*2m\s*\(1\+1\)')
    label, body = labelled(c(6, 'd'))
    assert 'Method +2 statements.' in body
    put(c(6, 'd'), 9, '1-3', 'career-exhibition-evaluation', component_rows(label,
        models(before_rate(body, r'3\s*@\s*3m\s*\(1\+1\+1\)'), 5), [[1, 1, 1]] * 3,
        'Original 3@3m(1+1+1), Method +2 statements. Three distinct complete responses, each method 1 and two statements 1 each; the method alone never earns all 3.'))
    for row in rows[c(6, 'd')]:
        for part, label in zip(row['parts'], ['Method', 'Statement 1', 'Statement 2']):
            part['verbatim'] = label
    assert set(rows) == set(raw) == set(PAGES) and len(rows) == 38 and sum(totals.values()) == 210

    case = select(tidy(paper_raw(paper, 8)), 'AMY’S CHOCOLATE', include=True)
    stems = {q: tidy(re.split(r'^Q\.\s*' + str(q) + r'\s+', paper_raw(paper, 14 + (q - 1) * 3), maxsplit=1, flags=re.M)[1].split('(a)', 1)[0]) for q in range(1, 7)}
    cards = []
    for k in raw:
        section, q, letter = k
        suffix = section.lower() + str(q) + (letter or '')
        card_id = 'lcvp-2017-cl-' + suffix
        ref = f'2017 CL Section {section} Q{q}' + (f'({letter})' if letter else '')
        pages = [PAGES[k]]
        if k in [a(5), b(2, 'a'), b(2, 'b'), b(2, 'c'), b(3, 'a'), b(3, 'b'), c(1, 'b'), c(5, 'b')]:
            pages.append(pages[0] + 1)
        card = dict(id=card_id, subjectId='lcvp', topicId='lcvp-link-modules-' + topics[k],
            conceptId=concept_id(card_id, concepts[k]), level='common', year=2017, section=section,
            questionRef=ref, questionText=question(paper, k), stem=case if section == 'B' else stems[q] if section == 'C' else '',
            figureKey='', labelKey=[], totalMarks=totals[k], rows=rows[k],
            tariffModel=dict(kind='fixed', notation='Original 2017 marking scheme allocation.'), sourceMaterial=source(pages))
        if section == 'C' and q in [1, 4] and letter in 'bcd':
            # These tasks refer to the career/business named in part(a).
            # Keep that printed instruction so each practice task is complete.
            card['stem'] += ' ' + question(paper, c(q, 'a'))
        if section == 'A':
            card['videoMaterial'] = dict(kind='source-video', label='OFFICIAL VIDEO', title='2017 LCVP audiovisual examination',
                playbackUrl=VIDEO_URL, canonicalUrl=VIDEO_URL, secFileid='LC462CLP031EV.mp4',
                attribution='State Examinations Commission — original 2017 Common Level English audiovisual recording.',
                presentationNote='Watch the original Work Experience sequence with its sound before answering. Follow the printed viewing instructions. Use the original source link if embedded playback is unavailable.')
            card['additionalSourceMaterials'] = [source([2], title='Original audiovisual instructions')]
        elif section == 'B':
            card['sourceMaterial'] = source([8], 'source-text', 'Amy’s Chocolate — complete case study')
            card['additionalSourceMaterials'] = [source(pages)]
        # The emitter omits empty optional notes; keep strict authored/runtime equality.
        for row in card['rows']:
            if row.get('contextNote') == '':
                row.pop('contextNote')
        cards.append(card)
    return cards, scheme


def scheme_page_text(scheme, number):
    # The original page8 native blocks retain each wrapped table cell.
    # Spatial sorting interleaves the two columns and breaks literal claims.
    return scheme[number - 1].get_text(sort=number != 8)


def write(cards, scheme):
    review = json.loads(REVIEW.read_text())
    proof = review['sourceVerification']['proof']
    digest = hashlib.sha256(json.dumps(cards, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    assert proof['tasks'] == review['manualPricedTasks'] == 38
    assert digest == proof['authoredSubsetSha256'], 'Refresh the mandatory original-source gate before writes'
    assert review['sourceVerification']['validatedAuthoringSha256'] == hashlib.sha256((ROOT / 'scripts/markbank/authoring/lcvp_review_2017.py').read_bytes()).hexdigest()
    path = ROOT / 'scripts/markbank/authored/lcvp.json'
    old = json.loads(path.read_text())
    prior = [c for c in old if c['year'] == 2017]
    preserved = [c for c in old if c['year'] != 2017]
    assert len(prior) in [0, 38] and len(preserved) == 398
    assert {c['id'] for c in prior} <= {c['id'] for c in cards}
    concepts = {c['id']: c['conceptId'] for c in prior}
    assert all(c['conceptId'] == concepts.get(c['id'], c['conceptId']) for c in cards)
    result, inserted = [], False
    for card in old:
        if card['year'] == 2017:
            if not inserted:
                result.extend(cards)
                inserted = True
        else:
            result.append(card)
    if not inserted:
        result.extend(cards)
    assert [c for c in result if c['year'] != 2017] == preserved
    assert {c['id'] for c in old} <= {c['id'] for c in result}
    path.write_text(json.dumps(result, ensure_ascii=False, indent=1) + '\n')
    pages = [f'## Physical page {i}\n\n' + scheme_page_text(scheme, i) for i, page in enumerate(scheme, 1)]
    text = '# SEC LCVP 2017 Common Level written marking scheme\n\n' + '\n\n'.join(pages)
    (ROOT / 'examiner-reports/lcvp/schemes/2017-cl.md').write_text('\n'.join(line.rstrip() for line in text.splitlines()).rstrip() + '\n')
    review['status'] = 'source-authored; independent-sweep-complete; validation-pending'
    review['tasks'] = [dict(id=c['id'], questionRef=c['questionRef'], marks=c['totalMarks'], topicId=c['topicId']) for c in cards]
    REVIEW.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    cards, scheme = build()
    if '--write' in sys.argv:
        write(cards, scheme)
    else:
        print(json.dumps(cards, ensure_ascii=False, indent=2))
