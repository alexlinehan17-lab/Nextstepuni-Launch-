#!/usr/bin/env python3
"""Hash-bound selectors following the independent 54-page 2016 visual sweep."""
import hashlib
import json
import re
import sys
import fitz
from lcvp_review_2026 import ROOT, tidy, select, point
from lcvp_review_2024 import split_raw
from lcvp_review_2022 import page_raw
from lcvp_review_2018 import choice_row, response_row, before_rate, models
from lcvp_review_2017 import paper_raw, header_body, component_rows
from lcvp_identity import concept_id

REVIEW = ROOT / 'scripts/markbank/authoring/lcvp/2016-cl-main-review.json'
PAPER = 'paper-trail-corpus/exampapers/2016/LC462CLPO00EV.pdf'
CASE = 'paper-trail-corpus/exampapers/2016/LC462CLPO16EV.pdf'
SCHEME = 'paper-trail-corpus/markingschemes/2016/LC462CLP000EV.pdf'
HASHES = {PAPER: 'fa035b6dea179a129bfc8654becd56f4f46e007c9b34826e1fc7987f92199903',
          CASE: '53eb749b342da6cc2a30322ee095edf6a32c215162d7abc6a2393eb3c380f213',
          SCHEME: 'c4d3e8b7ad6a6b16b7a19a3d3412ee001347045d7c97e02e44939f16a9d13838'}
VIDEO_URL = 'https://www.examinations.ie/archive/exampapers/2016/LC462CLP031EV.mp4'


def documents():
    for path, expected in HASHES.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
    return fitz.open(ROOT / PAPER), fitz.open(ROOT / SCHEME)


def key(section, q, letter=None, roman=None):
    return section, q, letter, roman


def scheme_parts(doc):
    value = '\n'.join(page_raw(doc, n) for n in range(4, 17))
    # Physical page7 repeats Q2 at the continuation. Remove only this known
    # repeated label in the selector, never in the original source transcript.
    assert len(re.findall(r'^\s*Q2\s+\(b\)', value, re.M)) == 1
    value = re.sub(r'^\s*Q2\s+(?=\(b\))', '', value, flags=re.M)
    sections = split_raw(value, r'^\s*Section ([ABC])\s+', list('ABC'))
    out = {}
    for section, value in sections.items():
        questions = split_raw(value, r'^\s*Q\.?\s*(\d+)\s*',
            [str(n) for n in range(1, {'A': 8, 'B': 3, 'C': 6}[section] + 1)])
        for q, block in questions.items():
            q = int(q)
            if section == 'A' or (section == 'B' and q == 1):
                out[key(section, q)] = block
            else:
                for letter, part in split_raw(block, r'^\s*\(([abcd])\)\s*',
                                             list('ab' if section == 'B' else 'abcd')).items():
                    if section == 'C' and (q, letter) in [(1, 'a'), (5, 'd')]:
                        # Each original block prints BOTH questions then BOTH
                        # answers. Preserve the right question/answer pairing.
                        markers = list(re.finditer(r'^\s*\((i{1,2})\)\s*', part, re.M))
                        assert [m[1] for m in markers] == ['i', 'ii', 'i', 'ii']
                        for index, roman in enumerate(['i', 'ii']):
                            heading = part[markers[index].end():markers[index + 1].start()]
                            answer = part[markers[index + 2].end():markers[index + 3].start() if index == 0 else len(part)]
                            out[key(section, q, letter, roman)] = heading + '\n' + answer
                    else:
                        out[key(section, q, letter)] = part
    assert len(out) == 39
    return out


PAGES = {key('A', q): [p] for q, p in enumerate([3, 3, 3, 4, 4, 5, 6, 7], 1)}
PAGES[key('A', 5)] = [4, 5]
PAGES.update({key('B', 1): [9], key('B', 2, 'a'): [10, 11], key('B', 2, 'b'): [10, 11],
              key('B', 3, 'a'): [11, 12], key('B', 3, 'b'): [11, 12]})
PAGES.update({key('C', q, letter): [14 + (q - 1) * 3 + {'a': 0, 'b': 0, 'c': 1, 'd': 2}[letter]]
              for q in range(1, 7) for letter in 'abcd'})
for q, letter in [(1, 'a'), (5, 'd')]:
    pages = PAGES.pop(key('C', q, letter))
    PAGES.update({key('C', q, letter, roman): pages for roman in ['i', 'ii']})
for k in [key('C', 1, 'b'), key('C', 2, 'b'), key('C', 4, 'b'), key('C', 5, 'b')]:
    PAGES[k].append(PAGES[k][0] + 1)


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
        value = re.split(r'\(i{1,2}\)\s*', value, maxsplit=1)[0]
    return tidy(re.sub(r'\b\d+\s+marks?\b', '', value, flags=re.I))


def contrast_models(scheme):
    raw = page_raw(scheme, 5)
    raw = raw.split('Manager', 1)[1].split('3 @ 2m', 1)[0]
    result = []
    for line in raw.splitlines():
        match = re.match(r'^\s*([1-4])\.\s+(.+?)\s{2,}(.+?)\s*$', line)
        if match:
            assert int(match[1]) == len(result) + 1
            result.append(tidy(match[2]) + ' — ' + tidy(match[3]))
    assert len(result) == 4, raw
    assert result[-1] == 'Tells them what to do — Facilities creativity'
    return result


def source(pages, kind='source-question', title='Original question'):
    return dict(kind=kind, label='OFFICIAL SOURCE', title=title, pages=pages,
        attribution='SEC LCVP Link Modules 2016 Common Level — © State Examinations Commission.',
        presentationNote='Read the complete original source and question in context.')


def build():
    paper, scheme = documents()
    raw = scheme_parts(scheme)
    rows, totals, topics, concepts = {}, {}, {}, {}
    a = lambda q: key('A', q)
    b = lambda q, l=None: key('B', q, l)
    c = lambda q, l, r=None: key('C', q, l, r)
    held = {b(2, 'a'), c(3, 'd')}
    def put(k, marks, topic, concept, value):
        rows[k], totals[k], topics[k], concepts[k] = value, marks, topic, concept
    def labelled(k):
        header, body = header_body(raw[k])
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

    _, body = labelled(a(1))
    put(a(1), 2, '1-1', 'medical-device-business', [point('product', tidy(before_rate(body, r'2\s*m')), 2,
        'The original complete answer receives 2 marks. No internal split is printed.')])
    ordinary(a(2), '1-0', 'senior-team-leader-role', 2, 1, 3, r'2\s*@\s*1m')
    ordinary(a(3), '0-0', 'competent-employee', 2, 1, 2, r'2\s*@\s*1m')
    ordinary(a(4), '1-0', 'effective-leadership-style', 2, 2, 3, r'2\s*@\s*2m')
    ordinary(a(5), '1-0', 'intrinsic-motivation', 2, 2, 3, r'2\s*@\s*2m', binary=True)
    rows[a(5)][0]['contextNote'] += ' Original 2@2m (0/2): no 1-mark partial.'
    ordinary(a(6), '1-0', 'team-motivation', 4, 1, 7, r'4\s*@\s*1m')
    put(a(7), 6, '1-0', 'manager-leader-contrasts', [choice_row('contrasts', question(paper, a(7)),
        contrast_models(scheme), 3, 2,
        'Original 3@2m (0/2). Each response must contain the complete manager–leader contrast; no isolated-cell credit or 1-mark partial. All four paired models remain. The printed phrase “Facilities creativity” is retained literally.')])
    label, body = labelled(a(8))
    preface = tidy(body[:re.search(r'^\s*1\.', body, re.M).start()])
    put(a(8), 6, '0-0', 'workplace-feedback-training', [choice_row('reasons', label,
        models(before_rate(body, r'6\s*@\s*1m'), 6), 6, 1,
        'Original 6@1m. ' + preface)])

    ordinary(b(1), '1-2', 'community-project-stakeholders', 3, 2, 12, r'3\s*@\s*2m', binary=True)
    label, body = labelled(b(2, 'a'))
    sub = split_raw(body, r'^\s*\((i{1,2})\)\s*', ['i', 'ii'])
    pools = [models(before_rate(sub['i'], r'2\s*@\s*1m'), 8), models(before_rate(sub['ii'], r'2\s*@\s*2m'), 9)]
    linkage = '(If not linked; mark both and disallow the lower mark)'
    assert linkage in tidy(sub['ii'])
    guidance = ('Numeric scoring held. One complete linked 6-mark task: (i) 2@1m; (ii) 2@2m (1+1). '
        + linkage + ' The source does not name the comparison operands. Keep both subasks tied to the chosen stakeholder, all original models and the literal linkage clause; confidence review only pending authoritative clarification. No deduction rule is inferred.')
    values = [point('contributions', 'Type of support discussed specific to the stakeholder chosen.', note=guidance)]
    values.extend(point(f'contribution-{i}', v) for i, v in enumerate(pools[0], 1))
    values.append(point('benefits', linkage))
    values.extend(point(f'benefit-{i}', v) for i, v in enumerate(pools[1], 1))
    put(b(2, 'a'), 6, '1-2', 'linked-stakeholder-contributions-benefits', values)
    ordinary(b(2, 'b'), '1-2', 'community-development-benefits', 3, 2, 7, r'3\s*@\s*2m')
    ordinary(b(3, 'a'), '1-3', 'long-term-project-planning', 3, 2, 7, r'3\s*@\s*2\s*marks')
    _, body = labelled(b(3, 'b'))
    assert 'Identify the project (1m)' in tidy(body)
    put(b(3, 'b'), 6, '1-3', 'other-community-project-evaluation', [point('project', 'Identify the project', 1),
        choice_row('evaluation', question(paper, b(3, 'b')), models(before_rate(body, r'5\s*@\s*1m'), 11), 5, 1,
            'Identify one OTHER project (1m) and evaluate its short and long term success (5@1m). Retain both time horizons without an invented fixed split; all eleven original models remain.')])

    _, body = labelled(c(1, 'a', 'i'))
    put(c(1, 'a', 'i'), 1, '1-0', 'named-entrepreneur', [point('name', tidy(before_rate(body, r'1m')), 1)])
    label, body = labelled(c(1, 'a', 'ii'))
    put(c(1, 'a', 'ii'), 4, '1-0', 'enterprising-definition', [response_row('definition', label,
        [tidy(before_rate(body, r'2\s*@\s*2m'))], 2, [0, 2],
        'Original 2@2m. Keep the complete slash-separated definition; no fixed semantic pairing or unprinted 1-mark step is inferred.')])
    label, body = labelled(c(1, 'b'))
    pool = ['Risk-takers', 'Innovative', 'Hardworking', 'Future-focused', 'Motivated', 'Determined', 'Decisive', 'Self-confident']
    assert all(v in body for v in pool) and 'List is not exhaustive' in body
    put(c(1, 'b'), 6, '1-0', 'entrepreneur-characteristics', [response_row('characteristics', label, pool, 3, [0, 1, 2],
        'Original 3@2m (1+1). List is not exhaustive. Preserve all eight models from both columns.')])
    ordinary(c(1, 'c'), '1-0', 'entrepreneur-business-reasons', 3, 2, 8, r'3\s*@\s*2m')
    ordinary(c(1, 'd'), '1-1', 'starting-business-challenges', 4, 2, 12, r'4\s*@\s*2m')
    ordinary(c(2, 'a'), '1-3', 'carwash-advertising', 4, 1, 10, r'4\s*@\s*1m')
    ordinary(c(2, 'b'), '1-3', 'carwash-enterprise-planning', 3, 2, 11, r'3\s*@\s*2m')
    rows[c(2, 'b')][0]['contextNote'] += ' Materials have already been purchased. Keep advertising in the original pool; the source excludes purchased materials, not advertising.'
    ordinary(c(2, 'c'), '1-3', 'carwash-student-benefits', 3, 2, 8, r'3\s*@\s*2m')
    ordinary(c(2, 'd'), '1-3', 'carwash-evaluation-methods', 3, 3, 7, r'3\s*@\s*3m')
    rows[c(2, 'd')][0]['contextNote'] += ' Original 3@3m (1+1+1). No repetition of points.'
    ordinary(c(3, 'a'), '0-3', 'work-placement-school-differences', 2, 2, 8, r'2\s*@\s*2m')
    ordinary(c(3, 'b'), '0-3', 'work-placement-outcomes', 3, 2, 9, r'3\s*@\s*2m')
    ordinary(c(3, 'c'), '0-0', 'workplace-safety-benefits', 3, 2, 6, r'3\s*@\s*2m')
    _, body = labelled(c(3, 'd'))
    pool = models(before_rate(body, r'4\s*@\s*2m'), 5)
    put(c(3, 'd'), 9, '0-3', 'work-placement-evaluation', [point(f'heading-{i}', v, note=(
        'Numeric scoring held. Evaluation in light of ALL FIVE original headings. Printed total 9; literal allocation “4 @ 2m (0/2)” and “1 @ 1m”. Neither source assigns these values to particular headings or supplies a choose/best-four/ordered-response rule. Preserve the complete evaluation; confidence review only pending authoritative clarification. No positional or claim-order weights are inferred.' if i == 1 else '')) for i, v in enumerate(pool, 1)])

    ordinary(c(4, 'a'), '0-1', 'recruitment-advertising', 4, 1, 10, r'4\s*items\s*@\s*1m')
    label, body = labelled(c(4, 'b'))
    definitions = before_rate(body, r'2\s*@\s*3m')
    heads = ['Interpersonal skills', 'Covering letter', 'References', 'Personnel Manager']
    pieces = split_raw(definitions, r'^\s*(Interpersonal skills|Covering letter|References|Personnel Manager):\s*', heads)
    pool = [h + ': ' + tidy(pieces[h]) for h in heads]
    put(c(4, 'b'), 6, '0-1', 'underlined-recruitment-terms', component_rows(label, pool, [[2, 1]] * 2,
        'Explain TWO distinct underlined terms from all FOUR shown. Original 2@3m (2+1), with no 1-of-2 component award. CV and equal opportunities employer are bold, not underlined.'))
    ordinary(c(4, 'c'), '0-4', 'standout-job-application', 3, 2, 8, r'3\s*@\s*2m')
    label, body = labelled(c(4, 'd'))
    periods = ['Before', 'On the day', 'During the interview']
    parts = split_raw(before_rate(body, r'3\s*@\s*3m'), r'^\s*(Before|On the day|During the interview):\s*\([BDI]\)', periods)
    put(c(4, 'd'), 9, '0-1', 'interview-preparation-periods', [choice_row(f'period-{i}', title,
        models(parts[title], count), 2, 2,
        'Original 3@3m (2+1), “2 points from each”. TWO distinct points under EACH required period; response slots 2 then 1, not fixed prices for named models. Retain every original example.', steps=[2, 1])
        for i, (title, count) in enumerate(zip(periods, [6, 4, 6]), 1)])
    ordinary(c(5, 'a'), '1-2', 'voluntary-visitor-meeting-planning', 3, 1, 5, r'3\s*@\s*1m')
    _, body = labelled(c(5, 'b'))
    pool = models(before_rate(body, r'1\s*m\s*-\s*heading'), 7)
    put(c(5, 'b'), 8, '1-2', 'voluntary-visitor-agenda', [point('heading', 'AGENDA', 1),
        choice_row('content', 'content', pool, 6, 1, 'Original 1m heading + 6@1m content + 1m Layout. Keep all seven content models for the first class meeting.'),
        point('layout', 'Layout', 1)])
    ordinary(c(5, 'c'), '1-2', 'voluntary-visitor-advance-planning', 3, 2, 6, r'3\s*@\s*2m')
    # The question pair shares an 8-mark header; original answer tariffs split
    # it 2 + 6. Do not attach the shared 8 to either separated task.
    body = raw[c(5, 'd', 'i')]
    answer = select(tidy(before_rate(body, r'2\s*@\s*1m')), 'Good presentation skills', include=True)
    put(c(5, 'd', 'i'), 2, '1-0', 'presentation-skills-importance', [response_row('importance', question(paper, c(5, 'd', 'i')),
        [answer], 2, [0, 1], 'Original 2@1m. Keep the whole slash-separated explanation; no fixed semantic division is inferred.')])
    ordinary(c(5, 'd', 'ii'), '1-0', 'effective-presentation', 3, 2, 6, r'3\s*@\s*2m')
    _, body = labelled(c(6, 'a'))
    assert re.fullmatch(r'Name:\s*1m\s+Outline:\s*2m\s*\+\s*1m', body.strip())
    outline = component_rows('Outline:', ['Outline: 2m + 1m'], [[2, 1]],
        'Name 1m, Outline 2m + 1m. Retain the same named local business and its product/service; no model enterprise or 1-of-2 component award is invented.')
    put(c(6, 'a'), 4, '1-1', 'local-business-product-service', [point('name', 'Name:', 1), *outline])
    ordinary(c(6, 'b'), '1-1', 'local-business-location', 3, 2, 10, r'3\s*@\s*2m')
    ordinary(c(6, 'c'), '1-1', 'business-success-measures', 3, 2, 7, r'3\s*@\s*2\s*\(1\+1\)')
    label, body = labelled(c(6, 'd'))
    put(c(6, 'd'), 9, '1-1', 'business-education-training', component_rows(label,
        models(before_rate(body, r'3\s*@\s*3m'), 7), [[2, 1]] * 3,
        'THREE distinct responses. Original 3@3m (2+1): separately controlled binary 0/2 component plus 0/1; no 1-of-2 award. All seven original models remain.'))
    assert set(rows) == set(raw) == set(PAGES) and len(rows) == 39
    assert sum(totals.values()) == 210 and sum(totals[k] for k in held) == 15

    case = select(tidy(paper_raw(paper, 8)), 'GLENOR COMMUNITY PROJECT', include=True)
    stems = {q: tidy(re.split(r'^Q\.\s*' + str(q) + r'\s+', paper_raw(paper, 14 + (q - 1) * 3), maxsplit=1, flags=re.M)[1].split('(a)', 1)[0]) for q in range(1, 7)}
    cards = []
    for k in raw:
        section, q, letter, roman = k
        suffix = section.lower() + str(q) + (letter or '') + (roman or '')
        card_id = 'lcvp-2016-cl-' + suffix
        ref = f'2016 CL Section {section} Q{q}' + (f'({letter})' if letter else '') + (f'({roman})' if roman else '')
        card = dict(id=card_id, subjectId='lcvp', topicId='lcvp-link-modules-' + topics[k],
            conceptId=concept_id(card_id, concepts[k]), level='common', year=2016, section=section,
            questionRef=ref, questionText=question(paper, k), stem=case if section == 'B' else stems[q] if section == 'C' else '',
            figureKey='', labelKey=[], totalMarks=totals[k], rows=rows[k],
            tariffModel=dict(kind='questionTotal' if k in held else 'fixed', notation='Original 2016 marking scheme allocation.'),
            sourceMaterial=source(PAGES[k]))
        if section == 'C' and q == 6 and letter in 'bcd':
            card['stem'] += ' ' + question(paper, c(6, 'a'))
        if section == 'A':
            card['videoMaterial'] = dict(kind='source-video', label='OFFICIAL VIDEO', title='2016 LCVP audiovisual examination',
                playbackUrl=VIDEO_URL, canonicalUrl=VIDEO_URL, secFileid='LC462CLP031EV.mp4',
                attribution='State Examinations Commission — original 2016 Common Level English audiovisual recording.',
                presentationNote='Watch the original Leadership sequence with its sound before answering. Follow the printed viewing instructions. Use the original source link if embedded playback is unavailable.')
            card['additionalSourceMaterials'] = [source([2], title='Original audiovisual instructions')]
        elif section == 'B':
            card['sourceMaterial'] = source([8], 'source-text', 'Glenor Community Project — complete case study')
            card['additionalSourceMaterials'] = [source(PAGES[k])]
            if k == b(2, 'a'):
                card['stem'] += ' ' + question(paper, b(1))
        elif section == 'C' and q == 4:
            card['sourceMaterial'] = source([23], 'source-text', 'Choco Ltd — complete original advertisement')
            card['sourceMaterial']['presentationNote'] += ' The four underlined terms are interpersonal skills, covering letter, references and Personnel Manager.'
            card['additionalSourceMaterials'] = [source(PAGES[k])]
        for row in card['rows']:
            if row.get('contextNote') == '':
                row.pop('contextNote')
        cards.append(card)
    return cards, scheme


def scheme_page_text(scheme, number):
    return scheme[number - 1].get_text(sort=True)


def write(cards, scheme):
    review = json.loads(REVIEW.read_text())
    proof = review['sourceVerification']['proof']
    digest = hashlib.sha256(json.dumps(cards, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    assert proof['tasks'] == review['manualPricedTasks'] == 39
    assert digest == proof['authoredSubsetSha256'], 'Refresh the mandatory original-source gate before writes'
    assert review['sourceVerification']['validatedAuthoringSha256'] == hashlib.sha256((ROOT / 'scripts/markbank/authoring/lcvp_review_2016.py').read_bytes()).hexdigest()
    path = ROOT / 'scripts/markbank/authored/lcvp.json'
    old = json.loads(path.read_text())
    preserved = [c for c in old if c['year'] != 2016]
    prior = [c for c in old if c['year'] == 2016]
    assert len(prior) in [0, 39] and len(preserved) == 436
    assert {c['id']: c['conceptId'] for c in prior}.items() <= {c['id']: c['conceptId'] for c in cards}.items()
    result, inserted = [], False
    for card in old:
        if card['year'] == 2016:
            if not inserted:
                result.extend(cards)
                inserted = True
        else:
            result.append(card)
    if not inserted:
        result.extend(cards)
    assert [c for c in result if c['year'] != 2016] == preserved
    path.write_text(json.dumps(result, ensure_ascii=False, indent=1) + '\n')
    pages = [f'## Physical page {n}\n\n' + scheme_page_text(scheme, n) for n in range(1, 21)]
    transcript = '# SEC LCVP 2016 Common Level written marking scheme\n\n' + '\n\n'.join(pages)
    (ROOT / 'examiner-reports/lcvp/schemes/2016-cl.md').write_text('\n'.join(line.rstrip() for line in transcript.splitlines()).rstrip() + '\n')
    review['status'] = 'source-authored; independent-sweep-complete; validation-pending'
    review['tasks'] = [dict(id=c['id'], questionRef=c['questionRef'], marks=c['totalMarks'], topicId=c['topicId']) for c in cards]
    REVIEW.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    cards, scheme = build()
    if '--write' in sys.argv:
        write(cards, scheme)
    else:
        print(json.dumps(cards, ensure_ascii=False, indent=2))
